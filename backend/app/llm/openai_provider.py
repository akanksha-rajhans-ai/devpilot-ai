import time

from openai import AsyncOpenAI

from app.core.config import get_settings
from app.llm.base import LLMProvider
from app.schemas.llm import LLMResult, LLMUsage


class OpenAILLMProvider(LLMProvider):
    name = "openai"

    def __init__(self):
        settings = get_settings()

        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required when LLM_PROVIDER=openai")

        self.model = settings.openai_model
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)

    async def generate(self, prompt: str) -> LLMResult:
        start_time = time.perf_counter()

        response = await self.client.responses.create(
            model=self.model,
            input=prompt,
        )

        latency_ms = (time.perf_counter() - start_time) * 1000
        usage = getattr(response, "usage", None)

        input_tokens = getattr(usage, "input_tokens", None) if usage else None
        output_tokens = getattr(usage, "output_tokens", None) if usage else None
        total_tokens = getattr(usage, "total_tokens", None) if usage else None

        return LLMResult(
            content=response.output_text,
            provider=self.name,
            model=self.model,
            latency_ms=latency_ms,
            usage=LLMUsage(
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                total_tokens=total_tokens,
            ),
        )