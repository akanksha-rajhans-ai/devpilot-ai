from app.core.config import get_settings
from app.embeddings.base import EmbeddingProvider
from app.embeddings.mock_provider import MockEmbeddingProvider
from app.embeddings.sentence_transformer_provider import (
    SentenceTransformerEmbeddingProvider,
)


def get_embedding_provider() -> EmbeddingProvider:
    settings = get_settings()
    provider_name = settings.embedding_provider.strip().lower()

    if provider_name == "mock":
        return MockEmbeddingProvider(
            dimension=settings.embedding_dimension,
        )

    if provider_name == "sentence_transformers":
        return SentenceTransformerEmbeddingProvider(
            model_name=settings.embedding_model,
            dimension=settings.embedding_dimension,
        )

    raise ValueError(
        f"Unsupported embedding provider: {provider_name}"
    )
