from pydantic import BaseModel, Field


class RetrievalEvaluationCase(BaseModel):
    question: str = Field(..., min_length=1)
    expected_document_id: str = Field(..., min_length=1)


class RetrievalEvaluationRequest(BaseModel):
    cases: list[RetrievalEvaluationCase]
    top_k: int = Field(default=4, ge=1, le=20)


class RetrievalEvaluationResponse(BaseModel):
    case_count: int
    hit_rate_at_k: float
    mean_reciprocal_rank: float
    failures: list[dict]
