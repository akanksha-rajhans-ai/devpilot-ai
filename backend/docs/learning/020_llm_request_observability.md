# 020 LLM Request Observability

## What Problem Did This Solve?

The platform needs visibility into LLM calls so engineers can understand provider usage, latency, token consumption, prompt versions, and request correlation without exposing sensitive prompt or response content.

## Why Was This Design Chosen?

We added a dedicated LLM observability utility that records safe metadata for every LLM call. This keeps model call logging centralized and avoids scattering logging logic across services.

## What Alternatives Exist?

- Log nothing
- Log raw prompts and responses
- Log only generic application messages
- Use OpenTelemetry spans immediately
- Use LangSmith immediately

## What Would Break If This Component Disappeared?

The team would have limited visibility into AI cost, latency, provider behavior, and prompt version usage. Debugging production AI issues would become much harder.

## How Would This Evolve At 10x Traffic?

LLM calls would emit OpenTelemetry spans, cost metrics, provider error rates, model fallback events, prompt version dashboards, and alerts on latency or token spikes.

## Interview Questions

1. Why should LLM observability avoid raw prompt logging?
2. What metadata should be captured for model calls?
3. How does prompt ID help debugging?
4. How do trace IDs connect API requests to LLM calls?
5. How would this evolve with LangGraph?