# ADR 0002: Structured Logging

## Status

Accepted

## Context

DevPilot AI needs a consistent logging approach before adding business logic, AI workflows, database access, or external tool integrations.

## Options Considered

1. Use `print()` statements
2. Use Python's built-in logging module
3. Use a third-party library such as structlog or loguru
4. Implement full OpenTelemetry logging immediately

## Decision

Use Python's built-in logging module with centralized configuration.

## Consequences

The application has a simple, standard logging foundation that works locally and in containers. The format is not yet JSON and does not yet include request IDs or trace IDs. Those capabilities will be added later as the observability layer matures.