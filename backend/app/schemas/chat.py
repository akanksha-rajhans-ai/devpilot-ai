from typing import Optional

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    answer: str
    provider: str
    model: str
    conversation_id: Optional[str] = None