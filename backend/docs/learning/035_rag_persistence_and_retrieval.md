# 035: RAG Persistence and Retrieval

## What Was Built

DevPilot now chunks documents, generates embeddings, persists document lineage,
ranks chunks, creates grounded prompts, and returns structured citations.

The repository boundary has in-memory and SQLAlchemy implementations. PostgreSQL
uses pgvector, while SQLite uses JSON vectors and Python cosine similarity.

## Why This Design

Embedding generation and vector storage are separate concerns. The embedding
provider defines the vector space; the repository stores and searches vectors;
the RAG service coordinates retrieval and generation.

This separation makes providers and databases replaceable and gives each layer
a focused test surface.

## Concepts to Explore

- Recall at K versus precision at K
- Chunk size, overlap, and parent-document retrieval
- Cosine distance versus inner product
- Exact versus approximate nearest-neighbor search
- HNSW construction and query parameters
- Re-embedding migrations when models change
- Hybrid retrieval and reranking
- Prompt injection through retrieved content

## Interview Questions

1. Why must query and document vectors use the same embedding model?
2. What is the difference between retrieval quality and generation quality?
3. When would HNSW be preferable to exact search?
4. Why return citations as structured fields rather than only prose?
5. How would you re-embed millions of chunks without downtime?
6. How do chunk size and overlap affect recall and context quality?
7. Why retain the original document after chunks are persisted?
8. How would tenant filtering interact with approximate vector indexes?

## Scale Evolution

At larger scale, ingestion becomes asynchronous and idempotent. Workers batch
embedding requests, write vectors transactionally, and send permanent failures
to a dead-letter queue. Retrieval gains metadata filters, hybrid ranking,
reranking, latency budgets, and offline quality gates.
