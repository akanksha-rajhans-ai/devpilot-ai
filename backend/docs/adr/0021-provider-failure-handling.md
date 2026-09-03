# ADR 0021: Provider Failure Handling

## Status

Accepted

## Context

DevPilot AI now calls LLM providers through a provider abstraction. External providers may fail, and the platform needs consistent API behavior and safe observability.

## Options Considered

1. Let provider failures become generic 500 errors
2. Catch provider errors inside each route
3. Introduce a provider-specific exception and centralized handler
4. Add retries, circuit breakers, and fallback immediately

## Decision

Introduce `LLMProviderError`, handle it centrally as a `502 Bad Gateway`, and record failed LLM call metadata.

## Consequences

Clients receive a stable provider failure response and operators can observe failed LLM calls. The implementation does not yet retry, fall back, or distinguish between timeout, rate limit, invalid credentials, and quota failures.