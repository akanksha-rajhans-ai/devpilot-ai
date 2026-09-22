import hashlib
import math
import re

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

        vector = [0.0] * self.dimension
        tokens = re.findall(r"[a-z0-9_]+", text.lower())

        for token in tokens:
            digest = hashlib.sha256(token.encode("utf-8")).digest()
            for index in range(self.dimension):
                vector[index] += (digest[index % len(digest)] / 127.5) - 1.0

        magnitude = math.sqrt(
            sum(value * value for value in vector)
        )

        if magnitude == 0:
            vector[0] = 1.0
            return vector

        return [value / magnitude for value in vector]
