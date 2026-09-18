# ADR 0034: Use SQLAlchemy for Database Session Management

## Status

Accepted

## Context

DevPilot AI needs a database foundation before documents, chunks, and
embeddings can be persisted in PostgreSQL and pgvector.

The application must support lightweight local development while preserving
a path to production PostgreSQL.

## Decision

DevPilot AI will use SQLAlchemy 2.x for database engines, sessions, ORM
mapping, and transaction management.

SQLite will remain the temporary local database.

PostgreSQL with the Psycopg driver will become the production database.

Database sessions will be created through a central session factory and
exposed to FastAPI through a generator dependency that always closes them.

## Consequences

### Positive

- Centralized database configuration
- Explicit transaction handling
- Request-scoped sessions
- Testable dependency boundaries
- Support for SQLite and PostgreSQL
- A foundation for Alembic and pgvector

### Negative

- Adds ORM and driver dependencies
- SQLite cannot reproduce every PostgreSQL behavior
- Session and transaction concepts require careful ownership
- PostgreSQL integration tests will still be necessary

## Alternatives

### Raw SQL Connections

Rejected as the primary approach because connection lifecycle, transactions,
mapping, and testing would require more application-owned infrastructure.

### Async SQLAlchemy

Deferred. The current API does not yet demonstrate database concurrency that
justifies the additional complexity of async drivers and async sessions.

The architecture can be revisited after measuring actual database workloads.

### PostgreSQL Only

Deferred locally because Docker is blocked on the managed Mac and PostgreSQL
availability has not yet been established.

Production behavior will still be validated against PostgreSQL before
deployment.

## Future Work

- Add Alembic migrations
- Create document and chunk ORM models
- Replace the in-memory document store
- Enable the pgvector extension
- Add vector columns and similarity search
- Add PostgreSQL integration tests