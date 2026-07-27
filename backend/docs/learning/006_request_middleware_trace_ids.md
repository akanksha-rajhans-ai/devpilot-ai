# 006 Request Middleware & Trace IDs

## What Problem Did This Solve?

The application needs a way to correlate client-facing responses with backend logs. A trace ID lets operators find all logs related to a single request.

## Why Was This Design Chosen?

We implemented ASGI middleware with a `ContextVar` so every request receives a trace ID that can be accessed by route handlers, exception handlers, and deeper service code.

## What Alternatives Exist?

- Generate IDs inside each route
- Store trace ID in `request.state`
- Use a third-party correlation ID package
- Add OpenTelemetry immediately

## What Would Break If This Component Disappeared?

Debugging production issues would become harder because logs from different requests could not be reliably connected to a client-reported failure.

## How Would This Evolve At 10x Traffic?

Trace IDs would propagate to downstream services, background jobs, LLM calls, vector database queries, and MCP tool executions. OpenTelemetry would provide distributed traces across service boundaries.

## Interview Questions

1. Why do distributed systems need trace IDs?
2. Why is a global variable unsafe for request-scoped data?
3. What does `ContextVar` solve in async Python?
4. How should trace IDs flow across service boundaries?
5. How does this support future AI observability?
