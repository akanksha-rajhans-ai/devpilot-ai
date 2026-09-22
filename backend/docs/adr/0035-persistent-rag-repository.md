# ADR 0035: Use a Repository Boundary for RAG Storage

## Status

Accepted

## Decision

RAG services depend on a document repository contract. In-memory storage supports
unit tests; SQLAlchemy supports SQLite and PostgreSQL. PostgreSQL uses pgvector
and an HNSW cosine index.

## Consequences

The service layer is portable and testable, but two search implementations must
remain behaviorally consistent. PostgreSQL integration tests are required before
production deployment.
