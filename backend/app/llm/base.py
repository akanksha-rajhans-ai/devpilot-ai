from abc import ABC, abstractmethod


class LLMProvider(ABC):
    name: str
    model: str

    @abstractmethod
    async def generate(self, prompt: str) -> str:
        pass