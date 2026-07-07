from app.llm.base import LLMProvider
from app.schemas.chat import ChatRequest, ChatResponse


class ChatService:
    def __init__(self, llm_provider: LLMProvider):
        self.llm_provider = llm_provider

    async def chat(self, request: ChatRequest) -> ChatResponse:
        answer = await self.llm_provider.generate(request.message)

        return ChatResponse(
            answer=answer,
            provider=self.llm_provider.name,
            model=self.llm_provider.model,
            conversation_id=request.conversation_id,
        )