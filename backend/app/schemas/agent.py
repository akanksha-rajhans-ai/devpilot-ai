from typing import Optional

from pydantic import BaseModel, Field

from app.schemas.document import Citation
from app.schemas.llm import LLMUsage


class AgentRunRequest(BaseModel):
    message: str = Field(..., min_length=1)
    thread_id: Optional[str] = None


class AgentRunResponse(BaseModel):
    status: str
    answer: Optional[str] = None
    error: Optional[str] = None
    approval_reason: Optional[str] = None
    plan: str
    workflow: str
    route: str
    thread_id: str
    provider: Optional[str] = None
    model: Optional[str] = None
    prompt_id: Optional[str] = None
    latency_ms: Optional[float] = None
    usage: Optional[LLMUsage] = None
    citations: list[Citation] = Field(default_factory=list)
    retrieval_count: int = 0
    tool_name: Optional[str] = None
    tool_result: Optional[dict] = None
