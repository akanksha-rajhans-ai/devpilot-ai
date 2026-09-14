# ADR 0029: Agent Audit Events

## Status

Accepted

## Context

DevPilot AI now has LangGraph workflows with routing, provider calls, retries, failure state, checkpointing, and approval stubs. Agent execution is security-relevant and should be traceable.

## Options Considered

1. No agent audit events yet
2. Audit only failed workflows
3. Audit workflow start and finish from the API endpoint
4. Audit every graph node immediately
5. Store audit records in a database immediately

## Decision

Audit agent workflow start and finish events using the existing audit utility.

## Consequences

Agent execution is now visible in audit logs with workflow, status, route, and thread ID. The current implementation does not yet include authenticated actor ID, node-level audit records, persistent storage, or SIEM integration.