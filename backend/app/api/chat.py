from fastapi import APIRouter

from app.llm.factory import get_llm_provider
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest):
    provider = get_llm_provider()
    service = ChatService(provider)
    return await service.chat(request)