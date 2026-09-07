from pydantic import BaseModel, Field

from app.schemas.llm import LLMUsage


class AgentRunRequest(BaseModel):
    message: str = Field(..., min_length=1)


class AgentRunResponse(BaseModel):
    answer: str
    plan: str
    workflow: str
    provider: str
    model: str
    prompt_id: str
    latency_ms: float
    usage: LLMUsage