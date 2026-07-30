# ADR 0012: JWT Token Service

## Status

Accepted

## Context

DevPilot AI needs authentication support for protected platform APIs. Before adding login routes or database-backed users, the project needs reusable token creation and verification utilities.

## Options Considered

1. Server-side sessions
2. Opaque bearer tokens
3. JWT access tokens
4. Managed identity provider only

## Decision

Implement JWT access token utilities using `python-jose`.

## Consequences

The API can issue and verify stateless access tokens. JWTs must be short-lived, signed with environment-specific secrets, and must not contain sensitive payload data. Future work should add refresh tokens, key rotation, issuer/audience validation, and enterprise identity provider integration.