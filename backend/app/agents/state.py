from typing import TypedDict

from app.schemas.llm import LLMUsage


class AgentState(TypedDict, total=False):
    user_message: str
    plan: str
    answer: str
    provider: str
    model: str
    prompt_id: str
    latency_ms: float
    usage: LLMUsage