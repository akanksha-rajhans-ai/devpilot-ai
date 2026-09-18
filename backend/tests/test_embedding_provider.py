import asyncio
import math

import pytest

from app.embeddings.mock_provider import MockEmbeddingProvider


def test_mock_embedding_has_configured_dimension():
    provider = MockEmbeddingProvider(dimension=8)

    vectors = asyncio.run(provider.embed(["RAG uses retrieval"]))

    assert len(vectors) == 1
    assert len(vectors[0]) == 8


def test_mock_embedding_is_deterministic():
    provider = MockEmbeddingProvider(dimension=8)

    first = asyncio.run(provider.embed(["same text"]))
    second = asyncio.run(provider.embed(["same text"]))

    assert first == second


def test_mock_embedding_supports_batches():
    provider = MockEmbeddingProvider(dimension=8)

    vectors = asyncio.run(
        provider.embed(["first chunk", "second chunk"])
    )

    assert len(vectors) == 2
    assert vectors[0] != vectors[1]


def test_mock_embedding_is_normalized():
    provider = MockEmbeddingProvider(dimension=8)

    vectors = asyncio.run(provider.embed(["normalized vector"]))
    magnitude = math.sqrt(
        sum(value * value for value in vectors[0])
    )

    assert magnitude == pytest.approx(1.0)


def test_mock_embedding_rejects_empty_text():
    provider = MockEmbeddingProvider()

    with pytest.raises(ValueError, match="empty text"):
        asyncio.run(provider.embed([""]))


def test_mock_embedding_rejects_invalid_dimension():
    with pytest.raises(ValueError, match="dimension"):
        MockEmbeddingProvider(dimension=0)
        