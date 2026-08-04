# ADR 0015: Audit Logging Basics

## Status

Accepted

## Context

DevPilot AI will include security-sensitive capabilities such as authenticated APIs, admin endpoints, AI workflow execution, document access, and MCP tool calls.

## Options Considered

1. No audit logging initially
2. Use normal application logs only
3. Add a small reusable audit logging utility
4. Implement database-backed audit events immediately

## Decision

Add a reusable audit logging utility that emits structured audit events through a dedicated audit logger.

## Consequences

Security-sensitive events can now be logged consistently with event name, outcome, actor ID, trace ID, and metadata. The current implementation logs to stdout and does not yet provide persistence, tamper resistance, retention policy, or SIEM integration.

