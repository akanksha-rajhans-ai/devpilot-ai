# ADR 0033: Introduce an Embedding Provider Abstraction

## Status

Accepted

## Date

2026-09-18

## Context

DevPilot AI is adding a retrieval-augmented generation pipeline.

After document ingestion and chunking, each chunk must be converted into a numerical vector. User questions must also be converted into vectors so that relevant chunks can be found through similarity search.

Several implementation options exist:

- Call a hosted embedding API directly
- Use a local Sentence Transformers model
- Allow a vector database such as Chroma to generate embeddings
- Use a framework-provided abstraction
- Define a small application-owned provider interface

The project currently requires deterministic tests that do not depend on external APIs, credentials, model downloads, network access, or usage fees.

The long-term architecture must support a production-grade semantic embedding model and PostgreSQL with pgvector.

## Decision

DevPilot AI will define an application-owned `EmbeddingProvider` interface.

The interface will accept batches of text and asynchronously return batches of vectors:

```python
async def embed(
    self,
    texts: list[str],
) -> list[list[float]]
```

The initial implementation will be `MockEmbeddingProvider`.

The mock provider will:

- Produce deterministic vectors
- Support configurable dimensions
- Normalize generated vectors
- Reject blank text
- Require no external service or model

Provider selection will be configuration-driven through an embedding provider factory.

The current configuration will use:

```text
EMBEDDING_PROVIDER="mock"
EMBEDDING_DIMENSION=8
```

Unit tests will continue to use the mock provider after real providers are introduced.

After the RAG foundation is complete, a real semantic embedding provider will be selected through evaluation. A free local model will be supported for development and application testing.

PostgreSQL with pgvector will be used for persistent vector storage and similarity search.

## Rationale

An application-owned interface provides a stable boundary with minimal complexity.

It allows DevPilot AI to:

- Develop the pipeline without external dependencies
- Run deterministic unit tests
- Replace embedding models through configuration
- Compare local and hosted providers
- Keep vector storage separate from vector generation
- Avoid coupling services directly to a provider SDK
- Add consistent observability and failure handling later

The interface is intentionally small because the application currently requires only batch text embedding.

## Consequences

### Positive

- Unit tests remain fast and deterministic.
- Provider changes do not require rewriting document services.
- Local and hosted models can implement the same contract.
- Provider-specific dependencies remain isolated.
- The project can add consistent metrics and errors around one interface.
- pgvector storage remains independent of embedding generation.

### Negative

- The project must maintain its own small abstraction.
- Provider-specific features may not fit the common interface.
- The mock provider does not provide meaningful semantic similarity.
- Additional integration tests will be required for real models.
- Model changes require explicit migration and re-embedding plans.

### Risks

A common interface can become too broad if it tries to expose every provider feature.

To reduce this risk, the interface will remain limited to application requirements. Provider-specific functionality will not be added without a demonstrated use case.

Another risk is accidental mixing of vectors from different models. The persistence layer must eventually record model identity and vector dimensions.

## Alternatives Considered

### Use Chroma’s Default Embedding Function

Chroma can automatically embed documents and queries.

This was not selected as the primary architecture because DevPilot AI plans to use PostgreSQL with pgvector and wants embedding generation to remain independent of vector storage.

Chroma may still be evaluated as an alternative vector-store adapter.

### Call OpenAI Directly from Services

This would reduce initial code but tightly couple document and retrieval services to OpenAI.

It would also make unit tests dependent on mocking a vendor SDK throughout the service layer.

### Use LangChain’s Embedding Abstraction

LangChain already supports multiple embedding providers.

This was not selected for the foundational boundary because the required interface is small, and an application-owned contract makes the underlying behavior easier to understand and test.

LangChain adapters may later be implemented behind the application interface.

### Use Sentence Transformers Immediately

A local model would produce meaningful embeddings without API charges.

It was deferred because downloading and loading a model adds dependency, resource, and test complexity before the embedding pipeline is established.

The model will be added after the provider contract and surrounding foundation are stable.

## Operational Notes

Real embedding providers should eventually expose metrics for:

- Batch size
- Request latency
- Failure count
- Retry count
- Provider name
- Model name
- Input volume
- Estimated cost

Production ingestion should support asynchronous processing, retryable failures, and idempotency.

## Migration Strategy

When changing the embedding model or vector dimension:

1. Register the new model configuration.
2. Create compatible vector storage if the dimension changes.
3. Re-embed existing document chunks.
4. Validate retrieval quality.
5. Switch query traffic to the new model and index.
6. Retire the old vectors after verification.

Existing and new embedding spaces should not be mixed during migration.

## Future Decisions

Separate ADRs will cover:

- Selection of the real embedding model
- PostgreSQL persistence
- pgvector schema and indexes
- Similarity metric selection
- Synchronous versus asynchronous embedding ingestion
- Embedding model migration and versioning

## Interview Discussion

The central design principle is separation of concerns:

```text
Embedding provider -> creates vectors
Vector store       -> persists and searches vectors
RAG service        -> coordinates retrieval and generation
```

This separation improves testability, portability, and operational clarity without requiring application services to understand provider-specific details.