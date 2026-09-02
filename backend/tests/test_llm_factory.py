import pytest

from app.core.config import get_settings
from app.llm.factory import get_llm_provider
from app.llm.mock_provider import MockLLMProvider


def test_factory_returns_mock_provider_by_default():
    get_settings.cache_clear()

    provider = get_llm_provider()

    assert isinstance(provider, MockLLMProvider)
    assert provider.name == "mock"


def test_factory_rejects_unknown_provider(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "unknown")
    get_settings.cache_clear()

    with pytest.raises(ValueError, match="Unsupported LLM provider"):
        get_llm_provider()

    monkeypatch.delenv("LLM_PROVIDER", raising=False)
    get_settings.cache_clear()


def test_openai_provider_requires_api_key(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "openai")
    monkeypatch.setenv("OPENAI_API_KEY", "")
    get_settings.cache_clear()

    with pytest.raises(ValueError, match="OPENAI_API_KEY is required"):
        get_llm_provider()

    monkeypatch.delenv("LLM_PROVIDER", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    get_settings.cache_clear()