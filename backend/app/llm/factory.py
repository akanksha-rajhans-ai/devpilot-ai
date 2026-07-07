from app.core.config import settings
from app.llm.base import LLMProvider
from app.llm.mock_provider import MockLLMProvider


def get_llm_provider() -> LLMProvider:
    if settings.llm_provider == "mock":
        return MockLLMProvider()

    raise ValueError(f"Unsupported LLM provider: {settings.llm_provider}")