# ADR 0013: Current User Dependency

## Status

Accepted

## Context

DevPilot AI needs protected API routes. The platform already has JWT utilities, but routes need a reusable way to extract and validate bearer tokens.

## Options Considered

1. Parse Authorization headers manually in each route
2. Use FastAPI dependencies with `HTTPBearer`
3. Use middleware-only authentication
4. Delegate route protection to an API gateway immediately

## Decision

Use a FastAPI dependency called `get_current_user` backed by `HTTPBearer` and JWT decoding.

## Consequences

Routes can declare authentication requirements cleanly. The current implementation returns identity from the JWT subject claim only. Future work will load users from the database, validate account state, enforce RBAC, and emit audit logs.