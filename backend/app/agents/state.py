from typing import TypedDict


class AgentState(TypedDict, total=False):
    user_message: str
    plan: str
    answer: str