# ADR 0005: Error Handling

## Status

Accepted

## Context

DevPilot AI needs consistent API error responses before adding authentication, database access, AI providers, external tools, and workflow orchestration.

## Options Considered

1. Use FastAPI default error responses
2. Add centralized FastAPI exception handlers
3. Use middleware-only error handling
4. Create a custom exception hierarchy immediately

## Decision

Use centralized FastAPI exception handlers for HTTP errors, validation errors, and unhandled exceptions.

## Consequences

Clients get a stable error contract and internal exceptions are logged without exposing sensitive details. More specific domain exceptions can be added later when the application has domain-specific workflows.