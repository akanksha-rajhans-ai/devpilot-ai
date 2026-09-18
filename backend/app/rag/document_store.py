from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4



@dataclass(frozen=True)
class StoredDocument:
    document_id: str
    title: str
    content: str
    created_at: datetime
    metadata: dict[str, str] = field(default_factory=dict)

@dataclass(frozen=True)
class StoredDocumentChunk:
    chunk_id: str
    document_id: str
    chunk_index: int
    content: str


class InMemoryDocumentStore:
    def __init__(self):
        self._documents: dict[str, StoredDocument] = {}
        self._chunks: dict[str, list[StoredDocumentChunk]] = {}

    def add_document(
        self,
        title: str,
        content: str,
        metadata: Optional[dict[str, str]] = None,
    ) -> StoredDocument:
        document = StoredDocument(
            document_id=str(uuid4()),
            title=title,
            content=content,
            created_at=datetime.now(timezone.utc),
            metadata=metadata or {},
        )

        self._documents[document.document_id] = document
        return document

    def get_document(self, document_id: str) -> Optional[StoredDocument]:
        return self._documents.get(document_id)

    def clear(self) -> None:
        self._documents.clear()
        self._chunks.clear()

    def add_chunks(
        self,
        document_id: str,
        chunks: list[StoredDocumentChunk],
    ) -> None:
        self._chunks[document_id] = chunks


    def get_chunks(
        self,
        document_id: str,
    ) -> list[StoredDocumentChunk]:
        return self._chunks.get(document_id, [])


document_store = InMemoryDocumentStore()