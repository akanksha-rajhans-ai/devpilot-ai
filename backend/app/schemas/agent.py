from pydantic import BaseModel, Field


class AgentRunRequest(BaseModel):
    message: str = Field(..., min_length=1)


class AgentRunResponse(BaseModel):
    answer: str
    plan: str
    workflow: str