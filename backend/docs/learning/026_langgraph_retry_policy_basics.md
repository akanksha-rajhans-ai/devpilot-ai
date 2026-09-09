# 026 LangGraph Retry Policy Basics

## What Problem Did This Solve?

The workflow needed a way to recover from transient LLM provider failures without retrying permanent failures blindly.

## Why Was This Design Chosen?

We added retryability metadata to `LLMProviderError` and configured LangGraph retry policies on the LLM answer nodes. Retryable provider errors are re-raised so LangGraph can retry the node, while non-retryable errors become safe workflow failure state.

## What Alternatives Exist?

- Retry every exception
- Never retry provider failures
- Implement retries manually inside provider classes
- Use HTTP client retry middleware
- Add circuit breakers immediately

## What Would Break If This Component Disappeared?

Temporary provider failures would cause avoidable workflow failures. Users would see failed workflows even when a quick retry could have recovered.

## How Would This Evolve At 10x Traffic?

Retries would use exponential backoff, jitter, provider-specific error classification, retry budgets, timeout policies, circuit breakers, fallback providers, and metrics for retry attempts and recovery rates.

## Interview Questions

1. What makes a failure retryable?
2. Why should invalid API keys not be retried?
3. Why should retry policy be node-specific?
4. What is backoff and why does jitter matter?
5. How would retries apply to MCP tools?