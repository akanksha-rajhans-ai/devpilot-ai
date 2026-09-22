from contextlib import contextmanager
from typing import Iterator

from app.core.config import get_settings
from app.db.session import SessionLocal
from app.rag.document_store import document_store
from app.rag.repository import DocumentRepository, SQLAlchemyDocumentRepository


@contextmanager
def repository_scope() -> Iterator[DocumentRepository]:
    settings = get_settings()

    if settings.document_repository == "memory":
        yield document_store
        return

    session = SessionLocal()
    try:
        yield SQLAlchemyDocumentRepository(session)
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
