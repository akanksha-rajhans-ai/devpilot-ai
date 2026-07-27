# ADR 0006: Request Trace IDs

## Status

Accepted

## Context

DevPilot AI will eventually execute multi-step workflows involving API routes, LangGraph nodes, retrievers, LLM providers, databases, and MCP tools. Operators need a way to correlate logs and errors for a single request.

## Options Considered

1. No trace IDs initially
2. Generate IDs directly in each endpoint
3. Use `request.state`
4. Use `ContextVar` in middleware
5. Add full OpenTelemetry immediately

## Decision

Add trace IDs using custom FastAPI middleware and `ContextVar`.

## Consequences

Every request now receives an `X-Trace-Id` response header, and logs/errors can include the same ID. This is not a full distributed tracing system yet, but it prepares the codebase for OpenTelemetry later.