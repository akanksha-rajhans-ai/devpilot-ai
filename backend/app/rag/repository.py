from __future__ import annotations

import math
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.db.models import DocumentChunkModel, DocumentModel
from app.rag.document_store import StoredDocument, StoredDocumentChunk


@dataclass(frozen=True)
class ChunkSearchResult:
    chunk: StoredDocumentChunk
    document_title: str
    score: float


class DocumentRepository(ABC):
    @abstractmethod
    def add_document(self, document: StoredDocument) -> None:
        pass

    @abstractmethod
    def add_chunks(self, chunks: list[StoredDocumentChunk]) -> None:
        pass

    @abstractmethod
    def get_document(self, document_id: str) -> Optional[StoredDocument]:
        pass

    @abstractmethod
    def list_documents(self, limit: int = 100) -> list[StoredDocument]:
        pass

    @abstractmethod
    def search_chunks(
        self,
        query_embedding: list[float],
        limit: int,
        min_similarity: float,
        embedding_provider: Optional[str] = None,
        embedding_model: Optional[str] = None,
    ) -> list[ChunkSearchResult]:
        pass


def cosine_similarity(left: list[float], right: list[float]) -> float:
    if len(left) != len(right):
        raise ValueError("Embedding dimensions do not match")

    left_norm = math.sqrt(sum(value * value for value in left))
    right_norm = math.sqrt(sum(value * value for value in right))
    if left_norm == 0 or right_norm == 0:
        return 0.0

    dot_product = sum(a * b for a, b in zip(left, right))
    return dot_product / (left_norm * right_norm)


class SQLAlchemyDocumentRepository(DocumentRepository):
    def __init__(self, session: Session):
        self.session = session

    def add_document(self, document: StoredDocument) -> None:
        self.session.add(
            DocumentModel(
                id=document.document_id,
                title=document.title,
                content=document.content,
                status=document.status,
                metadata_json=document.metadata,
                embedding_provider=document.embedding_provider,
                embedding_model=document.embedding_model,
                created_at=document.created_at,
            )
        )
        self.session.flush()

    def add_chunks(self, chunks: list[StoredDocumentChunk]) -> None:
        self.session.add_all(
            [
                DocumentChunkModel(
                    id=chunk.chunk_id,
                    document_id=chunk.document_id,
                    chunk_index=chunk.chunk_index,
                    content=chunk.content,
                    embedding=chunk.embedding,
                )
                for chunk in chunks
            ]
        )
        self.session.flush()

    def get_document(self, document_id: str) -> Optional[StoredDocument]:
        model = self.session.get(DocumentModel, document_id)
        return self._to_document(model) if model else None

    def list_documents(self, limit: int = 100) -> list[StoredDocument]:
        models = self.session.scalars(
            select(DocumentModel)
            .order_by(DocumentModel.created_at.desc())
            .limit(limit)
        ).all()
        return [self._to_document(model) for model in models]

    def search_chunks(
        self,
        query_embedding: list[float],
        limit: int,
        min_similarity: float,
        embedding_provider: Optional[str] = None,
        embedding_model: Optional[str] = None,
    ) -> list[ChunkSearchResult]:
        if self.session.bind is not None and self.session.bind.dialect.name == "postgresql":
            distance = DocumentChunkModel.embedding.cosine_distance(query_embedding)
            statement = select(
                DocumentChunkModel,
                DocumentModel.title,
                distance.label("distance"),
            ).join(DocumentModel)
            if embedding_provider:
                statement = statement.where(
                    DocumentModel.embedding_provider == embedding_provider
                )
            if embedding_model:
                statement = statement.where(DocumentModel.embedding_model == embedding_model)
            rows = self.session.execute(statement.order_by(distance).limit(limit)).all()
            return [
                ChunkSearchResult(
                    chunk=self._to_chunk(chunk),
                    document_title=title,
                    score=max(0.0, 1.0 - float(distance_value)),
                )
                for chunk, title, distance_value in rows
                if 1.0 - float(distance_value) >= min_similarity
            ]

        statement = select(DocumentChunkModel).options(
            selectinload(DocumentChunkModel.document)
        )
        if embedding_provider or embedding_model:
            statement = statement.join(DocumentModel)
        if embedding_provider:
            statement = statement.where(
                DocumentModel.embedding_provider == embedding_provider
            )
        if embedding_model:
            statement = statement.where(DocumentModel.embedding_model == embedding_model)
        models = self.session.scalars(statement).all()
        results = [
            ChunkSearchResult(
                chunk=self._to_chunk(model),
                document_title=model.document.title,
                score=cosine_similarity(query_embedding, list(model.embedding)),
            )
            for model in models
        ]
        return sorted(
            (result for result in results if result.score >= min_similarity),
            key=lambda result: result.score,
            reverse=True,
        )[:limit]

    @staticmethod
    def _to_document(model: DocumentModel) -> StoredDocument:
        return StoredDocument(
            document_id=model.id,
            title=model.title,
            content=model.content,
            created_at=model.created_at,
            metadata=model.metadata_json,
            status=model.status,
            embedding_provider=model.embedding_provider,
            embedding_model=model.embedding_model,
        )

    @staticmethod
    def _to_chunk(model: DocumentChunkModel) -> StoredDocumentChunk:
        return StoredDocumentChunk(
            chunk_id=model.id,
            document_id=model.document_id,
            chunk_index=model.chunk_index,
            content=model.content,
            embedding=list(model.embedding),
        )
