from app.llm.base import LLMProvider
from app.llm.mock_provider import MockLLMProvider
from app.core.config import get_settings

settings = get_settings()


def get_llm_provider() -> LLMProvider:
    if settings.llm_provider == "mock":
        return MockLLMProvider()

    raise ValueError(f"Unsupported LLM provider: {settings.llm_provider}")