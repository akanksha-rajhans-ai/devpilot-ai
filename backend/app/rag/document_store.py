from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional



@dataclass(frozen=True)
class StoredDocument:
    document_id: str
    title: str
    content: str
    created_at: datetime
    metadata: dict[str, str] = field(default_factory=dict)
    status: str = "ready"
    embedding_provider: str = "mock"
    embedding_model: str = "mock-lexical-v1"

@dataclass(frozen=True)
class StoredDocumentChunk:
    chunk_id: str
    document_id: str
    chunk_index: int
    content: str
    embedding: list[float] = field(default_factory=list)


class InMemoryDocumentStore:
    def __init__(self):
        self._documents: dict[str, StoredDocument] = {}
        self._chunks: dict[str, list[StoredDocumentChunk]] = {}

    def add_document(
        self,
        document: StoredDocument,
    ) -> None:
        self._documents[document.document_id] = document

    def get_document(self, document_id: str) -> Optional[StoredDocument]:
        return self._documents.get(document_id)

    def clear(self) -> None:
        self._documents.clear()
        self._chunks.clear()

    def add_chunks(
        self,
        chunks: list[StoredDocumentChunk],
    ) -> None:
        if not chunks:
            return
        self._chunks[chunks[0].document_id] = chunks


    def get_chunks(
        self,
        document_id: str,
    ) -> list[StoredDocumentChunk]:
        return self._chunks.get(document_id, [])

    def list_documents(self, limit: int = 100) -> list[StoredDocument]:
        documents = sorted(
            self._documents.values(),
            key=lambda document: document.created_at,
            reverse=True,
        )
        return documents[:limit]

    def search_chunks(
        self,
        query_embedding: list[float],
        limit: int,
        min_similarity: float,
        embedding_provider: Optional[str] = None,
        embedding_model: Optional[str] = None,
    ):
        from app.rag.repository import ChunkSearchResult, cosine_similarity

        results = []
        for chunks in self._chunks.values():
            for chunk in chunks:
                document = self._documents[chunk.document_id]
                if embedding_provider and document.embedding_provider != embedding_provider:
                    continue
                if embedding_model and document.embedding_model != embedding_model:
                    continue
                score = cosine_similarity(query_embedding, chunk.embedding)
                if score >= min_similarity:
                    results.append(
                        ChunkSearchResult(
                            chunk=chunk,
                            document_title=document.title,
                            score=score,
                        )
                    )

        return sorted(results, key=lambda result: result.score, reverse=True)[:limit]


document_store = InMemoryDocumentStore()
