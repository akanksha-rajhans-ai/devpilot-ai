# Milestone 3: AI Provider & LangGraph Foundation

## Summary

This milestone introduced DevPilot AI's first real AI platform capabilities.

The goal was not to build a chatbot. The goal was to create a production-shaped foundation for AI workflows using provider abstraction, prompt management, observability, failure handling, LangGraph orchestration, routing, retry behavior, checkpointing, approval gates, and audit events.

## Capabilities Added

### LLM Provider Abstraction

The platform introduced an `LLMProvider` interface so application code does not depend directly on a specific vendor SDK.

Implemented providers:

- Mock provider for tests and local development
- OpenAI provider for real hosted model calls

Why this matters:

- avoids vendor lock-in
- keeps CI independent from API keys
- supports future provider routing
- allows OpenAI, Gemini, Claude, Ollama, or LiteLLM later

### Prompt Management

Prompts were moved into a prompt registry with names and versions.

Examples:

- `chat.general:v1`
- `agent.answer:v1`
- `agent.code_explanation:v1`

Why this matters:

- prompts are application logic
- prompt versions support evaluation and rollback
- graph nodes can reference prompt IDs
- observability can track which prompt version was used

### LLM Observability

LLM calls now emit safe metadata:

- provider
- model
- prompt ID
- latency
- token usage
- trace ID

Raw prompts and raw responses are not logged.

Why this matters:

- supports cost tracking
- helps debug latency
- preserves privacy
- prepares for OpenTelemetry and LangSmith later

### Provider Failure Handling

Provider failures are translated into stable platform behavior.

For direct chat:

- provider failure returns HTTP `502`

For agent workflows:

- provider failure can become workflow state: `status=failed`

Why this matters:

- prevents raw SDK errors leaking to clients
- separates API failures from workflow failures
- prepares for retries, fallbacks, and circuit breakers

### LangGraph Minimal Orchestration

The first LangGraph workflow introduced graph state, nodes, edges, and compiled execution.

Initial nodes:

- plan
- answer

Why this matters:

- establishes workflow orchestration
- prepares for multi-step agents
- separates graph coordination from provider access

### LangGraph With LLM Provider

The graph answer node calls the `LLMProvider` abstraction rather than OpenAI directly.

Why this matters:

- LangGraph handles orchestration
- provider layer handles model access
- graph remains vendor-independent

### Conditional Routing

The graph can route requests to different nodes:

- `code_explanation`
- `general_answer`
- `needs_approval`

Why this matters:

- different request types need different workflows
- prepares for RAG routing
- prepares for MCP/tool routing
- keeps routing out of API handlers

### Retry Policy

Retryable provider errors can be retried at the graph node level.

Why this matters:

- transient failures should not always fail the workflow
- permanent failures should not be retried blindly
- prepares for provider resilience and fallback behavior

### Checkpointing

The graph now uses an in-memory checkpointer and accepts `thread_id`.

Why this matters:

- supports workflow persistence
- prepares for human approval
- enables future resume/debug behavior
- lays the foundation for memory

Current limitation:

- in-memory checkpointing is not production durable

Future direction:

- Postgres-backed checkpointing

### Human Approval Stub

Risky requests return:

```text
status=waiting_for_approval

No dangerous action is executed.
Why this matters:
- agents need safety gates
- tool execution should not be fully autonomous
- prepares for MCP tool approval
Agent Audit Events
Agent workflow start and finish are audited.
Audit metadata includes:
- workflow
- thread ID
- route
- outcome
Why this matters:
- agent execution is security-relevant
- future MCP actions must be auditable
- audit trails support enterprise trust
Current Agent Flow
POST /api/v1/agent/run
  -> trace middleware
  -> rate limiting
  -> audit workflow started
  -> LangGraph workflow
      -> plan node
      -> conditional router
          -> code_explanation node
          -> general_answer node
          -> needs_approval node
      -> LLM provider abstraction
      -> LLM observability
      -> retry policy for retryable failures
      -> checkpointing by thread_id
  -> audit workflow finished
  -> response
Key API Endpoints
POST /api/v1/chat
POST /api/v1/agent/run
Example Agent Response
{
  "status": "completed",
  "workflow": "conditional-langgraph:v3",
  "route": "code_explanation",
  "thread_id": "demo-thread-1",
  "provider": "mock",
  "model": "mock-dev-model",
  "prompt_id": "agent.code_explanation:v1"
}
Example Approval Response
{
  "status": "waiting_for_approval",
  "workflow": "conditional-langgraph:v3",
  "route": "needs_approval",
  "approval_reason": "Request may perform a sensitive or irreversible action."
}
Architecture Principles Demonstrated
Separation of Concerns
API routes do not call vendor SDKs directly.
Provider Independence
LLM access is isolated behind an interface.
Workflow Orchestration
LangGraph coordinates stateful multi-step execution.
Safe Observability
Metadata is logged without exposing raw prompts or responses.
Failure Isolation
Provider failures are translated into safe platform behavior.
Human Control
Sensitive requests can pause before action.
Auditability
Agent workflow activity is traceable.
Important Tradeoffs
In-Memory Checkpointing
Good for learning and tests, not production durable.
Future: Postgres checkpointer.
Keyword Routing
Simple and testable, but limited.
Future: classifier or planner-based routing.
Mock Provider State
Useful for simulating failures, but test state must be isolated.
Future: injectable test providers.
No Real Tool Execution Yet
Intentional.
Approval gates, audit logs, and routing came first.
Interview Questions
1. Why did you build provider abstraction before LangGraph?
2. Why should LangGraph not call OpenAI directly?
3. What is graph state?
4. How does conditional routing work?
5. Why does checkpointing require a thread ID?
6. Why are retries node-specific?
7. Why should raw prompts not be logged?
8. What is the difference between API failure and workflow failure?
9. Why does MCP need audit and approval controls?
10. How would this evolve for production?