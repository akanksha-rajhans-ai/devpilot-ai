# 023 LangGraph With LLM Provider

## What Problem Did This Solve?

The LangGraph workflow needed to call the existing LLM provider abstraction instead of returning deterministic text. This connects orchestration to model access while preserving separation of concerns.

## Why Was This Design Chosen?

The graph node calls the provider interface through the factory and uses the prompt registry. This keeps LangGraph responsible for workflow coordination, while provider classes handle vendor-specific model calls.

## What Alternatives Exist?

- Call OpenAI directly inside the graph node
- Keep the graph deterministic only
- Put all chat service logic inside the graph
- Use LangChain model wrappers immediately
- Build a separate service object for every graph node

## What Would Break If This Component Disappeared?

The graph would not demonstrate real AI orchestration. Future routing, RAG, and MCP flows would not have a reusable pattern for calling models from graph nodes.

## How Would This Evolve At 10x Traffic?

The graph would inject providers through dependencies or workflow context, add retries and fallbacks, stream responses, emit OpenTelemetry spans per node, and track cost by workflow, tenant, user, and prompt version.

## Interview Questions

1. Why should LangGraph call a provider interface instead of OpenAI directly?
2. What is the difference between orchestration and model access?
3. Why does the graph state include provider/model/token metadata?
4. How would you test this graph without API keys?
5. How will this prepare for RAG and MCP?