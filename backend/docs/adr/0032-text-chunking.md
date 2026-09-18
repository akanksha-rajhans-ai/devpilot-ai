# ADR 0032: Text Chunking

## Status

Accepted

## Context

DevPilot AI needs to prepare ingested documents for retrieval. Before embeddings and vector search, documents must be split into manageable chunks.

## Options Considered

1. Do not chunk documents
2. Use simple character-based chunking
3. Use token-based chunking immediately
4. Use semantic chunking immediately
5. Use LangChain text splitters immediately

## Decision

Start with a simple character-based chunker with overlap.

## Consequences

The chunking behavior is easy to understand and test. It is not yet token-aware, semantic, or content-type-specific. Future work may replace this with LangChain splitters or custom code-aware chunking.