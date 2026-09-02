# ADR 0017: LLM Provider Abstraction

## Status

Accepted

## Context

DevPilot AI will need to support multiple model providers and test AI-facing routes without relying on external APIs.

## Options Considered

1. Call a vendor SDK directly from API routes
2. Use a custom provider interface
3. Use LangChain immediately for provider abstraction
4. Use LiteLLM immediately for provider routing

## Decision

Create a custom `LLMProvider` interface with a mock provider first.

## Consequences

The platform can test AI-facing API behavior without API keys or network calls. The abstraction is intentionally small and may later wrap OpenAI, Gemini, Claude, Ollama, LangChain, or LiteLLM depending on routing needs.
