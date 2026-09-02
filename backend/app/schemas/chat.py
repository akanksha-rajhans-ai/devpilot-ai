from typing import Optional

from pydantic import BaseModel, Field

from app.schemas.llm import LLMUsage


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    answer: str
    provider: str
    model: str
    latency_ms: float
    usage: LLMUsage
    prompt_id: str
    conversation_id: Optional[str] = None