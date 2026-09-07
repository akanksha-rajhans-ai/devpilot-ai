# ADR 0024: LangGraph Conditional Routing

## Status

Accepted

## Context

DevPilot AI has a LangGraph workflow connected to the LLM provider layer. The platform needs to route different request types to different workflow nodes before adding RAG or MCP tools.

## Options Considered

1. Keep one generic answer node
2. Add conditional routing with keyword-based classification
3. Use an LLM classifier immediately
4. Route requests in the API layer
5. Use LangGraph `Command`

## Decision

Use LangGraph `add_conditional_edges` after the planning node with a simple deterministic router.

## Consequences

The workflow can now branch into specialist nodes while remaining easy to test. The current routing logic is simple and may be replaced by a classifier, policy engine, or planner-driven router later.