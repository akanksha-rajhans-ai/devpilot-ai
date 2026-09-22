from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import JSON, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.config import get_settings
from app.db.base import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


settings = get_settings()
embedding_type = JSON()

try:
    from pgvector.sqlalchemy import VECTOR

    embedding_type = embedding_type.with_variant(
        VECTOR(settings.embedding_dimension),
        "postgresql",
    )
except ImportError:
    if settings.document_repository == "database" and settings.database_url.startswith(
        "postgresql"
    ):
        raise RuntimeError(
            "The pgvector package is required for PostgreSQL vector storage"
        )


class DocumentModel(Base):
    __tablename__ = "documents"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="ready")
    metadata_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    embedding_provider: Mapped[str] = mapped_column(String(64), nullable=False)
    embedding_model: Mapped[str] = mapped_column(String(128), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=utc_now
    )

    chunks: Mapped[list[DocumentChunkModel]] = relationship(
        back_populates="document",
        cascade="all, delete-orphan",
        order_by="DocumentChunkModel.chunk_index",
    )


class DocumentChunkModel(Base):
    __tablename__ = "document_chunks"
    __table_args__ = (
        UniqueConstraint(
            "document_id",
            "chunk_index",
            name="uq_document_chunks_document_index",
        ),
    )

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    document_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    embedding: Mapped[list[float]] = mapped_column(embedding_type, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=utc_now
    )

    document: Mapped[DocumentModel] = relationship(back_populates="chunks")
