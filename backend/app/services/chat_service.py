from app.llm.base import LLMProvider
from app.schemas.chat import ChatRequest, ChatResponse


class ChatService:
    def __init__(self, llm_provider: LLMProvider):
        self.llm_provider = llm_provider

    async def chat(self, request: ChatRequest) -> ChatResponse:
        result = await self.llm_provider.generate(request.message)

        return ChatResponse(
            answer=result.content,
            provider=result.provider,
            model=result.model,
            latency_ms=result.latency_ms,
            usage=result.usage,
            conversation_id=request.conversation_id,
        )