import hashlib
import math

from app.embeddings.base import EmbeddingProvider


class MockEmbeddingProvider(EmbeddingProvider):
    name = "mock"

    def __init__(self, dimension: int = 8):
        if dimension <= 0:
            raise ValueError(
                "Embedding dimension must be greater than zero"
            )

        self.dimension = dimension

    async def embed(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        return [self._embed_text(text) for text in texts]

    def _embed_text(self, text: str) -> list[float]:
        if not text.strip():
            raise ValueError("Cannot embed empty text")

        digest = hashlib.sha256(text.encode("utf-8")).digest()

        vector = [
            (digest[index % len(digest)] / 127.5) - 1.0
            for index in range(self.dimension)
        ]

        magnitude = math.sqrt(
            sum(value * value for value in vector)
        )

        if magnitude == 0:
            return vector

        return [value / magnitude for value in vector]