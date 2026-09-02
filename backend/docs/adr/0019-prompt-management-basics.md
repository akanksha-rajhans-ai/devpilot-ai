# ADR 0019: Prompt Management Basics

## Status

Accepted

## Context

DevPilot AI now has an LLM provider abstraction and real provider integration. The platform needs a disciplined way to manage prompts before adding agents, RAG, and tool workflows.

## Options Considered

1. Hardcode prompts in route handlers
2. Hardcode prompts in service classes
3. Create a small in-code prompt registry
4. Use LangChain prompt templates immediately
5. Add an external prompt management system immediately

## Decision

Start with a small in-code prompt registry using named, versioned templates.

## Consequences

Prompt usage is centralized and testable. The current approach is simple and does not yet support dynamic prompt editing, approvals, A/B testing, or storage outside code.