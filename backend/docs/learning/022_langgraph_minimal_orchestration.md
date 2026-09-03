# 022 LangGraph Minimal Orchestration

## What Problem Did This Solve?

The platform needed a workflow orchestration layer for multi-step AI behavior. A direct chat call is simple, but agentic systems need stateful workflows with multiple nodes.

## Why Was This Design Chosen?

We introduced LangGraph with a minimal `StateGraph` containing a planning node and an answer node. This teaches graph state, nodes, edges, start/end markers, and compilation before adding RAG or tools.

## What Alternatives Exist?

- Keep direct service calls only
- Use LangChain chains
- Write custom workflow orchestration
- Use Celery workflows
- Use a managed agent runtime

## What Would Break If This Component Disappeared?

The platform would lack a structured way to coordinate multi-step AI workflows. RAG, tool use, retries, and human approval would become harder to reason about.

## How Would This Evolve At 10x Traffic?

The workflow would add routing, typed outputs, retries, checkpointing, streaming, human approval, observability spans, and isolated execution for long-running workflows.

## Interview Questions

1. Why use LangGraph instead of a direct LLM call?
2. What is graph state?
3. Why must a LangGraph graph be compiled before running?
4. What is the role of `START` and `END`?
5. How will this connect to RAG and MCP later?