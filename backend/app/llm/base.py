from abc import ABC, abstractmethod

from app.schemas.llm import LLMResult


class LLMProvider(ABC):
    name: str
    model: str

    @abstractmethod
    async def generate(self, prompt: str) -> LLMResult:
        pass