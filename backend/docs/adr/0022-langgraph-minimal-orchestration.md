# ADR 0022: LangGraph Minimal Orchestration

## Status

Accepted

## Context

DevPilot AI needs an orchestration layer for future agent workflows involving planning, routing, retrieval, tool execution, evaluation, retries, and human approval.

## Options Considered

1. Keep direct chat service calls
2. Use LangChain chains
3. Build custom orchestration
4. Introduce LangGraph incrementally

## Decision

Introduce LangGraph with a minimal two-node `StateGraph`.

## Consequences

The platform now has a workflow foundation without adding unnecessary complexity. The first graph is intentionally simple and does not yet call LLMs, RAG, MCP tools, or checkpointing.