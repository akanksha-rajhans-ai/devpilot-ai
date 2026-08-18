# 017 LLM Provider Abstraction

## What Problem Did This Solve?

The platform needs a clean way to call language models without coupling API routes directly to a specific vendor SDK.

## Why Was This Design Chosen?

We introduced an `LLMProvider` interface, a mock provider, a provider factory, and a chat service. This keeps model-specific logic outside route handlers and allows providers to be swapped through configuration later.

## What Alternatives Exist?

- Call vendor SDKs directly inside routes
- Use LangChain for all provider access immediately
- Use LiteLLM as the only abstraction layer
- Create separate endpoints for each provider

## What Would Break If This Component Disappeared?

The application would become tightly coupled to one provider. Tests would require real API keys or network calls, and switching models would require changes across route/business logic.

## How Would This Evolve At 10x Traffic?

The provider layer would support model routing, fallback providers, cost tracking, circuit breakers, retries, streaming, provider-specific rate limits, and tenant-specific model policies.

## Interview Questions

1. Why use a provider abstraction?
2. What is the Strategy Pattern?
3. Why start with a mock provider?
4. What metadata should an LLM response include?
5. How would this layer support OpenAI, Gemini, Claude, and Ollama?