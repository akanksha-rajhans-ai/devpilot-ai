from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class DocumentIngestRequest(BaseModel):
    title: str = Field(..., min_length=1)
    content: str = Field(..., min_length=1)
    metadata: dict[str, str] = Field(default_factory=dict)


class DocumentIngestResponse(BaseModel):
    document_id: str
    title: str
    status: str
    chunk_count: int
    embedding_provider: str
    embedding_model: str


class DocumentSummary(BaseModel):
    document_id: str
    title: str
    status: str
    created_at: datetime
    embedding_provider: str
    embedding_model: str


class Citation(BaseModel):
    citation_id: str
    document_id: str
    document_title: str
    chunk_id: str
    chunk_index: int
    content: str
    score: float


class RAGQueryRequest(BaseModel):
    question: str = Field(..., min_length=1)
    top_k: Optional[int] = Field(default=None, ge=1, le=50)


class RAGQueryResponse(BaseModel):
    answer: str
    citations: list[Citation]
    retrieval_count: int
    provider: str
    model: str
    prompt_id: str
