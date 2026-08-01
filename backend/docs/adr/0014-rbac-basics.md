# ADR 0014: RBAC Basics

## Status

Accepted

## Context

DevPilot AI will need to restrict sensitive platform operations such as admin APIs, document management, AI workflow execution, evaluation access, and MCP tool usage.

## Options Considered

1. No authorization layer initially
2. Hardcode role checks inside routes
3. Use a reusable FastAPI dependency factory for roles
4. Introduce a full policy engine immediately

## Decision

Add a simple RBAC foundation using a `require_roles` dependency factory and role claims from JWTs.

## Consequences

Routes can declare required roles clearly. The current approach is simple and testable, but roles are currently trusted from JWT claims. Future work should load roles from a trusted database or identity provider and may evolve toward permission-based or policy-based access control.