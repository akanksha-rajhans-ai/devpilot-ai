from app.rag.document_store import InMemoryDocumentStore
from app.schemas.document import DocumentIngestRequest, DocumentIngestResponse
from typing import Optional
from uuid import uuid4

from app.rag.chunker import SimpleTextChunker
from app.rag.document_store import StoredDocumentChunk


class DocumentService:
    def __init__(
        self,
        store,
        chunker: Optional[SimpleTextChunker] = None,
    ):
    self.store = store
    self.chunker = chunker or SimpleTextChunker()

    def ingest_document(
        self,
        request: DocumentIngestRequest,
    ) -> DocumentIngestResponse:
        document = self.store.add_document(
            title=request.title,
            content=request.content,
        )

        text_chunks = self.chunker.chunk_text(request.content)

        stored_chunks = [
            StoredDocumentChunk(
                chunk_id=str(uuid4()),
                document_id=document_id,
                chunk_index=chunk.chunk_index,
                content=chunk.content,
            )
            for chunk in text_chunks
        ]

        self.store.add_chunks(document_id, stored_chunks)

        return DocumentIngestResponse(
            document_id=document.document_id,
            title=document.title,
            status="ingested",
            chunk_count=len(stored_chunks),
        )

    