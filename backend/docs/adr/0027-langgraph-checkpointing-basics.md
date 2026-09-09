# ADR 0027: LangGraph Checkpointing Basics

## Status

Accepted

## Context

DevPilot AI needs workflow persistence before adding human approval, memory, RAG, and MCP tool workflows.

## Options Considered

1. Continue without checkpointing
2. Use in-memory checkpointing
3. Add SQLite checkpointing
4. Add Postgres checkpointing immediately

## Decision

Use LangGraph `InMemorySaver` for local checkpointing basics.

## Consequences

The workflow now requires a `thread_id` when invoked. State can persist during the process lifetime, but checkpoints are lost on restart. Production should use a persistent checkpointer such as Postgres.