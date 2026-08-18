from typing import Optional

from pydantic import BaseModel


class LLMUsage(BaseModel):
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None
    total_tokens: Optional[int] = None


class LLMResult(BaseModel):
    content: str
    provider: str
    model: str
    latency_ms: float
    usage: LLMUsage