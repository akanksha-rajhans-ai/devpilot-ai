from pydantic import BaseModel, Field


class DocumentIngestRequest(BaseModel):
    title: str = Field(..., min_length=1)
    content: str = Field(..., min_length=1)


class DocumentIngestResponse(BaseModel):
    document_id: str
    title: str
    status: str