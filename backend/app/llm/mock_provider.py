from app.llm.base import LLMProvider


class MockLLMProvider(LLMProvider):
    name = "mock"
    model = "mock-dev-model"

    async def generate(self, prompt: str) -> str:
        return f"Mock response to: {prompt}"