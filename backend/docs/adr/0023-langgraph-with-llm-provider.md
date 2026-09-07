# ADR 0023: LangGraph With LLM Provider

## Status

Accepted

## Context

DevPilot AI has a minimal LangGraph workflow, an LLM provider abstraction, prompt registry, and LLM observability. The workflow needs to call the provider abstraction without coupling graph logic to a vendor SDK.

## Options Considered

1. Keep graph output deterministic
2. Call OpenAI directly from the graph node
3. Call the existing LLM provider abstraction from the graph node
4. Move all chat service logic into LangGraph

## Decision

Update the LangGraph answer node to use the prompt registry and LLM provider abstraction.

## Consequences

The workflow now performs model-backed orchestration while keeping vendor-specific details outside LangGraph. The graph still does not include conditional routing, retries, checkpointing, RAG, or MCP tools.