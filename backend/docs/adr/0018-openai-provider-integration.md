# ADR 0018: OpenAI Provider Integration

## Status

Accepted

## Context

DevPilot AI now has an `LLMProvider` abstraction and a mock provider. The platform needs a real hosted model provider while preserving testability and provider independence.

## Options Considered

1. Keep only the mock provider
2. Call OpenAI directly from the chat route
3. Implement OpenAI as an `LLMProvider`
4. Use LangChain or LiteLLM immediately

## Decision

Implement OpenAI as a provider adapter that conforms to the existing `LLMProvider` interface.

## Consequences

The platform can call OpenAI when configured, while tests and CI continue to use the mock provider. The current provider does not yet include retries, streaming, timeout policies, or circuit breakers.