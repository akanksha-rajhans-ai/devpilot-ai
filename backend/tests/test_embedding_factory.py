import pytest

from app.core.config import get_settings
from app.embeddings.factory import get_embedding_provider
from app.embeddings.mock_provider import MockEmbeddingProvider


def test_factory_returns_mock_embedding_provider():
    get_settings.cache_clear()

    provider = get_embedding_provider()

    assert isinstance(provider, MockEmbeddingProvider)
    assert provider.name == "mock"
    assert provider.dimension == 8


def test_factory_rejects_unknown_embedding_provider(
    monkeypatch,
):
    monkeypatch.setenv("EMBEDDING_PROVIDER", "unknown")
    get_settings.cache_clear()

    with pytest.raises(
        ValueError,
        match="Unsupported embedding provider",
    ):
        get_embedding_provider()

    monkeypatch.delenv(
        "EMBEDDING_PROVIDER",
        raising=False,
    )
    get_settings.cache_clear()