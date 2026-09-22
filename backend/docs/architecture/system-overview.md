# DevPilot AI System Architecture

## System Context

```text
Developer
   |
   v
NGINX workbench
   |
   v
FastAPI gateway -----------------------------------+
   |                                               |
   +-> identity, RBAC, rate limits, trace IDs      +-> metrics and traces
   |
   v
LangGraph orchestrator
   |
   +-> direct/code answer -> LLM provider
   +-> knowledge answer -> retrieval -> LLM provider -> citations
   +-> tool action -> permission policy -> MCP/local tool -> audit event
   +-> risky action -> human approval boundary

Knowledge ingestion
   document -> chunker -> embedding provider -> repository
                                                |
                           SQLite JSON / PostgreSQL pgvector
```

## Architectural Boundaries

- API schemas are transport contracts, not database models.
- Services own use-case orchestration.
- Repositories own persistence and vector search.
- Providers isolate model vendors.
- LangGraph owns agent state transitions and retries.
- The tool registry owns permissions before MCP transport is involved.
- Prompts are versioned assets rather than strings scattered through services.

## Ingestion Sequence

1. Validate the document request.
2. Create a stable document identity.
3. Split source text into overlapping chunks.
4. Embed chunks in one batch.
5. Persist the document, chunks, model identity, and vectors in one unit of work.
6. Return chunk and model metadata to the caller.

## Retrieval Sequence

1. Embed the question using the same embedding space as the chunks.
2. Rank chunks by cosine similarity.
3. Apply the top-K and similarity thresholds.
4. Label retrieved evidence with citation IDs.
5. Place evidence inside explicit untrusted-data delimiters.
6. Ask the LLM to answer only from that evidence.
7. Return the generated answer and machine-readable citations separately.

## Local and Production Modes

| Concern | Local learning | Production target |
|---|---|---|
| Repository | In-memory or SQLite | RDS PostgreSQL |
| Vectors | JSON plus Python cosine | pgvector plus HNSW |
| Embeddings | Deterministic mock | Evaluated local/hosted model |
| LLM | Mock | OpenAI/Bedrock adapter |
| Cache | Optional local Redis | ElastiCache Redis |
| Runtime | Python or Compose | EKS and Helm |
| Telemetry | Logs/console spans | OTel Collector, CloudWatch, dashboards |

## Trust Boundaries

- Retrieved documents are data and cannot override system instructions.
- Tools are allow-listed and assigned explicit permissions.
- Read-only tools may execute automatically.
- Sensitive or irreversible requests stop at an approval state.
- Provider credentials are configuration secrets, never prompt content.
- Audit events record authorization, agent runs, and tool execution.

## Known Production Follow-ups

- Replace in-memory LangGraph checkpoints with durable PostgreSQL/Redis storage.
- Move ingestion to a queue for large documents and backpressure.
- Add tenant IDs and row-level authorization before multi-tenant use.
- Evaluate a real embedding model and migrate vector dimensions deliberately.
- Add hybrid lexical/vector retrieval and reranking after establishing a baseline.
- Replace local rate limiting with Redis-backed atomic counters.
