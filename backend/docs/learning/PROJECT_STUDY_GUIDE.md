# DevPilot AI Study Guide

Use this guide after running the application. Read code in request-flow order,
change one behavior, and rerun the focused tests before moving on.

## Session 1: Platform Request Lifecycle

Trace `app/main.py`, middleware, exception handlers, configuration, and health
checks. Explain middleware ordering, trace context, rate limiting, and dependency
injection.

Exercise: send the same request with and without `X-Trace-Id` and follow the logs.

## Session 2: Provider Boundaries

Trace the LLM and embedding base classes, factories, mock implementations, and
OpenAI adapter. Explain dependency inversion, deterministic tests, batching,
timeouts, and retry ownership.

Exercise: add a provider configuration error and describe where it should fail.

## Session 3: LangGraph

Draw every node and conditional edge in `app/agents/workflow.py`. Separate state,
control flow, checkpointing, provider retries, and human approval.

Exercise: add a new documentation route without changing existing node behavior.

## Session 4: RAG Ingestion

Follow a document through validation, chunking, embedding, repository writes, and
the migration schema. Explain why the source document and embedding model identity
are retained.

Exercise: compare retrieval after changing chunk size and overlap.

## Session 5: RAG Retrieval

Follow a question through query embedding, cosine ranking, top-K selection,
prompt construction, generation, and citation serialization.

Exercise: create five documents and identify a query where mock lexical retrieval
fails. This demonstrates why a real model and evaluation dataset matter.

## Session 6: MCP and Tool Safety

Trace tool discovery, authorization, execution, auditing, and MCP transport.
Explain why a model is not an authorization system.

Exercise: design a write tool and list every control required before enabling it.

## Session 7: Evaluation

Build a small golden dataset and calculate hit rate at K and reciprocal rank by
hand. Separate retrieval failure from generation failure.

Exercise: compare top K values and describe the latency/context trade-off.

## Session 8: Observability

Connect trace IDs, logs, metrics, and spans. Define SLIs for agent completion,
provider latency, retrieval no-hit rate, tool errors, and token cost.

Exercise: propose an SLO and error-budget policy for the agent API.

## Session 9: Persistence and Distributed Systems

Compare the in-memory and SQLAlchemy repositories. Explain transactions,
connection pools, migration jobs, retries, idempotency, queues, and eventual
consistency.

Exercise: design asynchronous ingestion with a queue and dead-letter policy.

## Session 10: Cloud Deployment

Render the Helm chart and explain every workload, probe, resource request, HPA,
PDB, service, ingress path, and secret. Map each dependency to its AWS managed
service.

Exercise: describe a canary release and the metrics that would stop promotion.

## Executive Interview Questions

1. Where are the system's trust boundaries?
2. Which operations are strongly consistent, and which can be eventually consistent?
3. How does the design prevent vendor lock-in without creating useless abstractions?
4. What happens when the LLM succeeds but retrieval is wrong?
5. How would you operate model and embedding migrations without downtime?
6. What state prevents this service from scaling horizontally today?
7. How does human approval survive process restarts in a production design?
8. Why is MCP not itself a security boundary?
9. Which quality and reliability metrics belong in a launch gate?
10. When would you choose ECS over EKS for this platform?
