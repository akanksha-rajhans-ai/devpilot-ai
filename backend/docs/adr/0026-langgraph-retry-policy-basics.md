# ADR 0026: LangGraph Retry Policy Basics

## Status

Accepted

## Context

DevPilot AI has LangGraph workflows that call LLM providers. Some provider failures are transient and should be retried, while others are permanent and should fail safely.

## Options Considered

1. No retries
2. Retry all provider failures
3. Add manual retries inside graph nodes
4. Use LangGraph node retry policies
5. Add circuit breakers immediately

## Decision

Use LangGraph `RetryPolicy` on LLM answer nodes and classify provider errors with a `retryable` flag.

## Consequences

Transient provider failures can recover automatically, while permanent failures are still returned as workflow failure state. The implementation is simple and does not yet include exponential backoff tuning, circuit breakers, timeout policies, fallback models, or retry budgets.