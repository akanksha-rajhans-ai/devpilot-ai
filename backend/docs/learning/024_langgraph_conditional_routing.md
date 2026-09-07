# 024 LangGraph Conditional Routing

## What Problem Did This Solve?

The workflow needed the ability to choose different execution paths based on request type. This is the first step toward agentic orchestration where different nodes handle different categories of work.

## Why Was This Design Chosen?

We used LangGraph conditional edges after the planning node. The routing function reads graph state and returns the next node name, keeping routing logic separate from answer generation.

## What Alternatives Exist?

- One generic answer node for every request
- Route inside the API endpoint
- Use an LLM to classify every request
- Use LangGraph `Command` for update plus routing
- Use a separate router service

## What Would Break If This Component Disappeared?

The agent would treat all requests the same. Future RAG, MCP tools, code review, debugging, and evaluation paths would be harder to model cleanly.

## How Would This Evolve At 10x Traffic?

Routing would use richer classifiers, confidence thresholds, fallback behavior, per-route metrics, and human approval for sensitive paths. Expensive routes could have stricter rate limits and cost budgets.

## Interview Questions

1. What are conditional edges in LangGraph?
2. Why keep routing outside the API route?
3. When would you use deterministic routing versus LLM-based routing?
4. How does graph state influence routing?
5. How will conditional routing support RAG and MCP?