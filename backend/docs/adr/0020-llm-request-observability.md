# ADR 0020: LLM Request Observability

## Status

Accepted

## Context

DevPilot AI now has a provider abstraction, OpenAI provider integration, and prompt management. The platform needs safe visibility into LLM usage before adding agents, RAG, and MCP tools.

## Options Considered

1. Do not log LLM calls yet
2. Log raw prompts and responses
3. Log safe LLM metadata through a dedicated utility
4. Add full OpenTelemetry and LangSmith immediately

## Decision

Record safe LLM call metadata using a centralized observability utility.

## Consequences

The platform can track provider, model, prompt version, latency, token usage, and trace ID without exposing sensitive prompt or response content. Full distributed tracing and AI observability tools will be added later.