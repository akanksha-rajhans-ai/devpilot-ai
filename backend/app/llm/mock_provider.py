import time

from app.llm.base import LLMProvider
from app.llm.errors import LLMProviderError
from app.schemas.llm import LLMResult, LLMUsage

transient_failure_attempts: dict[str, int] = {}


class MockLLMProvider(LLMProvider):
    name = "mock"
    model = "mock-dev-model"

    async def generate(self, prompt: str) -> LLMResult:
        if "__simulate_provider_failure__" in prompt:
            raise LLMProviderError(
                message="Mock provider failed",
                provider=self.name,
                model=self.model,
                retryable=False,
            )

        if "__simulate_transient_provider_failure__" in prompt:
            attempts = transient_failure_attempts.get(prompt, 0)
            transient_failure_attempts[prompt] = attempts + 1

            if attempts == 0:
                raise LLMProviderError(
                    message="Mock provider transient failure",
                    provider=self.name,
                    model=self.model,
                    retryable=True,
                )

        start_time = time.perf_counter()

        content = f"Mock response to: {prompt}"
        latency_ms = (time.perf_counter() - start_time) * 1000

        input_tokens = len(prompt.split())
        output_tokens = len(content.split())

        return LLMResult(
            content=content,
            provider=self.name,
            model=self.model,
            latency_ms=latency_ms,
            usage=LLMUsage(
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                total_tokens=input_tokens + output_tokens,
            ),
        )