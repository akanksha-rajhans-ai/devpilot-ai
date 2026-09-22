from abc import ABC, abstractmethod


class EmbeddingProvider(ABC):
    name: str
    dimension: int

    @abstractmethod
    async def embed(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        """Convert a batch of texts into vectors."""
        pass
