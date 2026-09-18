import pytest

from app.rag.chunker import SimpleTextChunker


def test_short_text_creates_one_chunk():
    chunker = SimpleTextChunker(chunk_size=100, chunk_overlap=10)

    chunks = chunker.chunk_text("Short document")

    assert len(chunks) == 1
    assert chunks[0].chunk_index == 0
    assert chunks[0].content == "Short document"


def test_long_text_creates_overlapping_chunks():
    chunker = SimpleTextChunker(chunk_size=10, chunk_overlap=2)

    chunks = chunker.chunk_text("abcdefghijklmnopqrstuvwxyz")

    assert len(chunks) == 3
    assert chunks[0].content == "abcdefghij"
    assert chunks[1].content == "ijklmnopqr"
    assert chunks[2].content == "qrstuvwxyz"


def test_blank_text_returns_no_chunks():
    chunker = SimpleTextChunker()

    assert chunker.chunk_text("   ") == []


def test_overlap_must_be_smaller_than_chunk_size():
    with pytest.raises(ValueError):
        SimpleTextChunker(chunk_size=10, chunk_overlap=10)