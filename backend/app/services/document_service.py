from app.rag.document_store import InMemoryDocumentStore
from app.schemas.document import DocumentIngestRequest, DocumentIngestResponse


class DocumentService:
    def __init__(self, store: InMemoryDocumentStore):
        self.store = store

    def ingest_document(
        self,
        request: DocumentIngestRequest,
    ) -> DocumentIngestResponse:
        document = self.store.add_document(
            title=request.title,
            content=request.content,
        )

        return DocumentIngestResponse(
            document_id=document.document_id,
            title=document.title,
            status="ingested",
        )