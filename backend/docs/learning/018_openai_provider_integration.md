# 018 OpenAI Provider Integration

## What Problem Did This Solve?

The platform needed a real LLM provider implementation behind the existing provider interface, without coupling routes or services directly to a vendor SDK.

## Why Was This Design Chosen?

We implemented OpenAI as an adapter that conforms to the `LLMProvider` interface. Provider selection remains configuration-driven through `LLM_PROVIDER`.

## What Alternatives Exist?

- Call OpenAI directly from routes
- Use LangChain immediately
- Use LiteLLM for provider routing
- Add all providers at once
- Keep only the mock provider

## What Would Break If This Component Disappeared?

The platform would only support mock AI responses and could not call a real hosted model. If implemented incorrectly, vendor-specific code could leak into services and routes.

## How Would This Evolve At 10x Traffic?

The provider layer would add retries, timeouts, streaming, circuit breakers, cost tracking, fallback providers, model routing, tenant policies, and provider-specific rate limits.

## Interview Questions

1. Why keep OpenAI behind an interface?
2. Why should CI avoid real LLM calls?
3. What happens if the API key is missing?
4. How would you handle OpenAI downtime?
5. How would this provider connect to LangGraph later?