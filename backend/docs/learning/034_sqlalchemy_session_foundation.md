# 034: SQLAlchemy Session Foundation

## Problem

DevPilot AI requires persistent storage for documents, chunks, vectors,
users, audit records, and future workflow state.

Directly opening database connections inside endpoints would spread
connection management and transaction handling throughout the codebase.

## Solution

The application now has a central SQLAlchemy database layer consisting of:

- A declarative ORM base
- A configurable database engine
- A session factory
- A request-scoped session dependency

SQLite remains the local development database. PostgreSQL will become the
production database without requiring business services to manage database
driver details.

## Important Concepts

### Engine

The SQLAlchemy engine manages database connectivity and connection pooling.
It is normally created once per application process.

### Session

A session represents a unit of database work. It tracks ORM objects and
coordinates queries, inserts, updates, commits, and rollbacks.

A session is not the same thing as a raw database connection.

### Transaction

A transaction groups database operations into one atomic unit.

If the transaction commits, all operations succeed together. If it rolls
back, its uncommitted changes are discarded.

### Session Factory

`SessionLocal` creates sessions with consistent configuration.

It is a factory rather than a globally shared session because sessions should
not be shared across concurrent requests.

### Dependency Lifecycle

`get_db_session()` yields a session and closes it in a `finally` block.

This prevents connection leaks even when request processing raises an
exception.

### Connection Pooling

A connection pool reuses existing database connections instead of creating
a new network connection for every request.

`pool_pre_ping=True` detects stale connections before they are assigned to
application work.

## Why SQLite and PostgreSQL?

SQLite provides a simple local database without a separate server.

PostgreSQL provides production features including:

- Concurrent access
- Robust transactions
- Operational tooling
- Replication and recovery
- AWS RDS support
- pgvector extensions

SQLite tests provide useful feedback, but PostgreSQL integration tests will
still be required because the databases do not behave identically.

## What Would Break Without This Layer?

Without a central database layer:

- Endpoints could leak connections.
- Transaction behavior would become inconsistent.
- Tests would be harder to isolate.
- Switching database environments would require widespread changes.
- Repository code could create engines repeatedly.
- Concurrent requests might accidentally share sessions.

## Evolution at 10x Traffic

At higher traffic, the system may require:

- Connection pool tuning
- Database query metrics
- Slow-query monitoring
- Read replicas
- Transaction timeout policies
- Retry handling for transient failures
- PgBouncer or RDS Proxy
- Separate worker and API connection pools

## Common Mistakes

- Creating an engine for every request
- Sharing one session across requests
- Forgetting to close sessions
- Forgetting to commit writes
- Committing inside every repository method
- Using SQLite behavior as proof of PostgreSQL correctness
- Storing database credentials in source control

## Interview Questions

### What is the difference between an engine and a session?

The engine manages database connectivity and pooling. A session represents
a unit of work and coordinates ORM operations and transactions.

### Why should sessions not be global?

Sessions contain mutable transaction and object-tracking state. Sharing one
across requests can cause race conditions and transaction contamination.

### Why use dependency injection for sessions?

It gives each request a controlled session lifecycle and makes tests able to
replace the production session dependency.

### What is a transaction?

A transaction groups operations so they commit or roll back as one unit.

### Why is connection pooling important?

Opening database connections is expensive. Pooling reuses established
connections and limits resource consumption.

### Why use `pool_pre_ping`?

It detects stale pooled connections before application code tries to use them.

### Why are SQLite tests not sufficient for PostgreSQL?

The databases differ in types, concurrency, locking, SQL behavior,
extensions, and constraint handling.

### Where should commits occur?

Transaction boundaries generally belong in the service or unit-of-work layer,
where the complete business operation is known.