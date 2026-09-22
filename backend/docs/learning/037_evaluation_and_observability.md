# 037: Evaluation and Observability

## What Was Built

The platform calculates retrieval hit rate at K and mean reciprocal rank. It
also exposes Prometheus metrics, structured logs, trace IDs, and optional
OpenTelemetry FastAPI instrumentation.

## Why Both Are Required

Operational observability answers whether the system is healthy. AI evaluation
answers whether the system is useful and grounded. Low latency does not imply a
correct answer, and a strong offline score does not imply production reliability.

## Interview Questions

1. What is the difference between an SLI, SLO, and SLA?
2. What does mean reciprocal rank measure?
3. Why should RAG evaluation separate retrieval and generation?
4. How do traces help debug multi-step agent workflows?
5. Which metric detects a rising no-evidence answer rate?
6. How would you evaluate faithfulness without trusting an LLM judge blindly?
7. Why must golden datasets be versioned?
8. How would you detect model-quality regressions during a canary release?
