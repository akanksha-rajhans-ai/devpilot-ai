# 025 LangGraph Provider Failure Path

## What Problem Did This Solve?

The LangGraph workflow needed a way to represent handled provider failures as workflow state instead of always crashing the HTTP request.

## Why Was This Design Chosen?

We added `status` and `error` fields to graph state and converted provider failures into safe workflow failure responses. This separates API transport success from workflow execution success.

## What Alternatives Exist?

- Let provider errors bubble up as HTTP 502
- Return HTTP 500 for all graph failures
- Add retries immediately
- Use a dedicated failure node
- Use LangGraph conditional error routing

## What Would Break If This Component Disappeared?

The frontend would not be able to distinguish between API failure and agent workflow failure. Future retries, fallbacks, and human approval paths would be harder to model.

## How Would This Evolve At 10x Traffic?

Failures would include failed node, retryability, provider error type, timeout metadata, fallback attempts, and OpenTelemetry spans. The graph could route failures to retry, fallback, or human review nodes.

## Interview Questions

1. What is the difference between HTTP success and workflow success?
2. Why might a handled agent failure still return HTTP 200?
3. How would you model retryable versus non-retryable provider failures?
4. When would you prefer HTTP 502 instead?
5. How does this prepare for tool/MCP failures?