# ADR 0031: Document Ingestion Skeleton

## Status

Accepted

## Context

DevPilot AI is beginning its RAG milestone. Before chunking, embeddings, vector search, and citations, the platform needs a stable document ingestion boundary.

## Options Considered

1. Start directly with embeddings and vector search
2. Add a simple ingestion API and in-memory store first
3. Add Postgres and object storage immediately
4. Combine ingestion, chunking, and indexing into one feature

## Decision

Start with a document ingestion API backed by an in-memory document store.

## Consequences

The RAG pipeline now has a clear entry point. The implementation is not durable and will need to evolve to persistent metadata storage, object storage, chunking, embeddings, and indexing status.