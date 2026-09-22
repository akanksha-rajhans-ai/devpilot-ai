from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

from app.core.config import Settings, get_settings
from app.embeddings.base import EmbeddingProvider
from app.embeddings.factory import get_embedding_provider
from app.rag.chunker import SimpleTextChunker
from app.rag.document_store import (
    StoredDocument,
    StoredDocumentChunk,
)
from app.rag.repository import DocumentRepository
from app.schemas.document import (
    DocumentIngestRequest,
    DocumentIngestResponse,
)


class DocumentService:
    def __init__(
        self,
        store: DocumentRepository,
        chunker: Optional[SimpleTextChunker] = None,
        embedding_provider: Optional[EmbeddingProvider] = None,
        settings: Optional[Settings] = None,
    ):
        self.store = store
        self.chunker = chunker or SimpleTextChunker()
        self.embedding_provider = embedding_provider or get_embedding_provider()
        self.settings = settings or get_settings()

    async def ingest_document(
        self,
        request: DocumentIngestRequest,
    ) -> DocumentIngestResponse:
        document_id = str(uuid4())
        document = StoredDocument(
            document_id=document_id,
            title=request.title,
            content=request.content,
            created_at=datetime.now(timezone.utc),
            metadata=request.metadata,
            embedding_provider=self.embedding_provider.name,
            embedding_model=self.settings.embedding_model,
        )
        text_chunks = self.chunker.chunk_text(request.content)
        embeddings = await self.embedding_provider.embed(
            [chunk.content for chunk in text_chunks]
        )
        if len(embeddings) != len(text_chunks):
            raise ValueError("Embedding provider returned an unexpected vector count")

        stored_chunks = [
            StoredDocumentChunk(
                chunk_id=str(uuid4()),
                document_id=document_id,
                chunk_index=chunk.chunk_index,
                content=chunk.content,
                embedding=embedding,
            )
            for chunk, embedding in zip(text_chunks, embeddings)
        ]

        self.store.add_document(document)
        self.store.add_chunks(stored_chunks)

        return DocumentIngestResponse(
            document_id=document.document_id,
            title=document.title,
            status="ingested",
            chunk_count=len(stored_chunks),
            embedding_provider=self.embedding_provider.name,
            embedding_model=self.settings.embedding_model,
        )
