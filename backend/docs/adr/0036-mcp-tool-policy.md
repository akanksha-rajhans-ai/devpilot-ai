# ADR 0036: Keep Tool Policy Outside MCP and the LLM

## Status

Accepted

## Decision

Every tool is registered with an application-owned permission and approval
requirement. MCP transports schemas and calls, while the executor enforces policy
and records audit events.

## Consequences

Tool safety does not depend on prompt compliance. New tools require explicit
registration and executor logic, which is intentional review friction.
