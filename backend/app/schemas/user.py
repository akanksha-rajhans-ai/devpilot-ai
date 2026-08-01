from pydantic import BaseModel, Field


class CurrentUser(BaseModel):
    id: str
    roles: list[str] = Field(default_factory=list)