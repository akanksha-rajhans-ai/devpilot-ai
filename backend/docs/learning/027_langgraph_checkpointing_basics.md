# 027 LangGraph Checkpointing Basics

## What Problem Did This Solve?

The workflow needed a way to persist graph state by thread ID. Checkpointing is the foundation for memory, human approval, workflow resume, and time travel debugging.

## Why Was This Design Chosen?

We used LangGraph's `InMemorySaver` because it teaches checkpointing without introducing a database yet.

## What Alternatives Exist?

- No checkpointing
- SQLite checkpointing
- Postgres checkpointing
- Managed LangSmith deployment checkpointing

## What Would Break If This Component Disappeared?

The platform could not resume workflows, support human-in-the-loop approvals, or maintain thread-level graph state.

## How Would This Evolve At 10x Traffic?

In-memory checkpointing would be replaced by Postgres-backed checkpointing with retention, encryption, cleanup jobs, and tenant isolation.

## Interview Questions

1. What is a LangGraph checkpoint?
2. Why does checkpointing require a thread ID?
3. Why is in-memory checkpointing not production-ready?
4. How does checkpointing support human approval?
5. How is checkpointing different from long-term memory?