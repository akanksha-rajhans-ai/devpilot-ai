# 021 Provider Failure Handling

## What Problem Did This Solve?

The platform needs to handle LLM provider failures consistently. External AI providers can fail due to timeouts, rate limits, invalid credentials, quota exhaustion, or outages.

## Why Was This Design Chosen?

We introduced a custom `LLMProviderError`, centralized FastAPI handling for provider failures, and failure observability in the chat service. This keeps provider failure translation consistent and safe.

## What Alternatives Exist?

- Let provider exceptions bubble up as generic 500 errors
- Catch all exceptions inside the route
- Return raw provider error messages to clients
- Add retries/circuit breakers immediately
- Use provider-specific error classes only

## What Would Break If This Component Disappeared?

Clients would receive inconsistent errors, internal provider details could leak, and operators would have weaker visibility into failed model calls.

## How Would This Evolve At 10x Traffic?

Provider failures would include retryability metadata, timeout handling, exponential backoff, circuit breakers, fallback providers, provider-specific rate limit handling, and SLO-based alerts.

## Interview Questions

1. Why is provider failure usually a 502 instead of a 500?
2. What provider details are safe to return to clients?
3. Why log provider failure metadata but not raw prompts?
4. How would retries change this design?
5. How would this failure handling work inside LangGraph?