import asyncio

from app.embeddings.base import EmbeddingProvider


class SentenceTransformerEmbeddingProvider(EmbeddingProvider):
    name = "sentence_transformers"

    def __init__(self, model_name: str, dimension: int):
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as exc:
            raise RuntimeError(
                "Install requirements-ml.txt to use Sentence Transformers"
            ) from exc

        self.model_name = model_name
        self.dimension = dimension
        self._model = SentenceTransformer(model_name)
        actual_dimension = self._model.get_sentence_embedding_dimension()
        if actual_dimension != dimension:
            raise ValueError(
                f"Configured embedding dimension {dimension} does not match "
                f"model dimension {actual_dimension}"
            )

    async def embed(self, texts: list[str]) -> list[list[float]]:
        if any(not text.strip() for text in texts):
            raise ValueError("Cannot embed empty text")
        if not texts:
            return []

        embeddings = await asyncio.to_thread(
            self._model.encode,
            texts,
            normalize_embeddings=True,
        )
        return [embedding.tolist() for embedding in embeddings]
