from dataclasses import dataclass


@dataclass(frozen=True)
class TextChunk:
    chunk_index: int
    content: str


class SimpleTextChunker:
    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
    ):
        if chunk_size <= 0:
            raise ValueError("chunk_size must be greater than 0")

        if chunk_overlap < 0:
            raise ValueError(
                "chunk_overlap must be greater than or equal to 0"
            )

        if chunk_overlap >= chunk_size:
            raise ValueError(
                "chunk_overlap must be smaller than chunk_size"
            )

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_text(self, text: str) -> list[TextChunk]:
        normalized_text = text.strip()

        if not normalized_text:
            return []

        chunks = []
        start = 0
        chunk_index = 0

        while start < len(normalized_text):
            end = min(start + self.chunk_size, len(normalized_text))
            chunk_content = normalized_text[start:end]

            chunks.append(
                TextChunk(
                    chunk_index=chunk_index,
                    content=chunk_content,
                )
            )

            if end == len(normalized_text):
                break

            start = end - self.chunk_overlap
            chunk_index += 1

        return chunks