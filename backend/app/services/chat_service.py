from app.llm.base import LLMProvider
from app.prompts.registry import get_prompt_template
from app.schemas.chat import ChatRequest, ChatResponse


class ChatService:
    def __init__(self, llm_provider: LLMProvider):
        self.llm_provider = llm_provider

    async def chat(self, request: ChatRequest) -> ChatResponse:
        prompt_template = get_prompt_template("chat.general")
        prompt = prompt_template.render(message=request.message)

        result = await self.llm_provider.generate(prompt)

        return ChatResponse(
            answer=result.content,
            provider=result.provider,
            model=result.model,
            latency_ms=result.latency_ms,
            usage=result.usage,
            prompt_id=prompt_template.prompt_id,
            conversation_id=request.conversation_id,
        )