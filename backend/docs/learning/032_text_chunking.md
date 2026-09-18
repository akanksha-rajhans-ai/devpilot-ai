# 032 Text Chunking

## What Problem Did This Solve?

The RAG pipeline needs to split documents into smaller chunks before embedding and retrieval. Searching entire documents is too coarse and may exceed model or embedding context limits.

## Why Was This Design Chosen?

We added a simple character-based chunker with configurable chunk size and overlap. This keeps the concept clear before introducing token-aware or semantic chunking.

## What Alternatives Exist?

- No chunking
- Fixed character chunking
- Token-based chunking
- Sentence or paragraph chunking
- Semantic chunking
- Code-aware chunking

## What Would Break If This Component Disappeared?

Embeddings and retrieval would operate on entire documents, making search less precise and increasing the risk of irrelevant context being passed to the model.

## How Would This Evolve At 10x Traffic?

The chunker would become token-aware, content-type-aware, and possibly semantic. Code files, Markdown, PDFs, and API docs may each need different chunking strategies.

## Interview Questions

1. Why does RAG need chunking?
2. What is chunk overlap?
3. What happens if chunks are too small?
4. What happens if chunks are too large?
5. Why might code need a different chunking strategy than prose?