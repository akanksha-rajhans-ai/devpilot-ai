from typing import TypedDict

from app.schemas.llm import LLMUsage


class AgentState(TypedDict, total=False):
    user_message: str
    plan: str
    route: str
    status: str
    error: str
    approval_reason: str
    answer: str
    provider: str
    model: str
    prompt_id: str
    latency_ms: float
    usage: LLMUsage
    citations: list[dict]
    retrieval_count: int
    tool_name: str
    tool_result: dict
