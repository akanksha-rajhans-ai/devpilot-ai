from app.core.config import get_settings
from app.llm.base import LLMProvider
from app.llm.mock_provider import MockLLMProvider
from app.llm.openai_provider import OpenAILLMProvider


def get_llm_provider() -> LLMProvider:
    settings = get_settings()

    if settings.llm_provider == "mock":
        return MockLLMProvider()

    if settings.llm_provider == "openai":
        return OpenAILLMProvider()

    raise ValueError(f"Unsupported LLM provider: {settings.llm_provider}")