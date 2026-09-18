# 033: Embedding Provider Abstraction

## Feature Summary

This feature introduces a provider-independent interface for generating text embeddings.

The first implementation is a deterministic mock embedding provider. It allows the embedding pipeline to be developed and tested without downloading a machine-learning model, calling an external API, managing credentials, or incurring cost.

A real embedding model will be integrated after the RAG foundation is complete.

## What Problem Does This Solve?

A RAG system must convert document chunks and user questions into numerical vectors.

These vectors allow the system to determine which document chunks are semantically related to a question.

Without an abstraction, application services could become directly dependent on one embedding vendor or library:

```python
openai.embeddings.create(...)
```

That would make the system harder to test and more expensive to change.

The abstraction allows application code to use a stable contract:

```python
vectors = await provider.embed(texts)
```

The application does not need to know whether the vectors came from:

- A deterministic mock
- Sentence Transformers
- OpenAI
- Amazon Bedrock
- A self-hosted embedding service
- Another future provider

## What Is an Embedding?

An embedding is a list of floating-point numbers representing characteristics of an input.

Example:

```text
"RAG combines retrieval and generation"

-> [0.12, -0.31, 0.08, ...]
```

Texts with similar meanings should produce vectors that are close together according to a similarity metric.

Common similarity metrics include:

- Cosine similarity
- Euclidean distance
- Inner product

The mock provider does not understand semantic meaning. It only produces deterministic vectors for testing the application pipeline.

## Architecture

```text
Document text
    -> TextChunker
    -> EmbeddingProvider
        -> MockEmbeddingProvider
        -> Future SentenceTransformerProvider
        -> Future OpenAIEmbeddingProvider
    -> Vector storage
        -> Future PostgreSQL with pgvector
```

## Components

### EmbeddingProvider

`EmbeddingProvider` is an abstract base class defining the contract every embedding provider must implement.

Its primary method is:

```python
async def embed(
    self,
    texts: list[str],
) -> list[list[float]]
```

The input is a batch of strings.

The output is a list of vectors, with one vector corresponding to each input string.

### Why Batch Inputs?

Production embedding APIs commonly support batching.

Batching can:

- Reduce network calls
- Reduce request overhead
- Improve throughput
- Simplify rate-limit management
- Reduce cost for some providers

The contract therefore accepts multiple texts even when a caller currently has only one.

### MockEmbeddingProvider

The mock provider generates deterministic vectors using SHA-256.

Deterministic means:

```text
same input + same configuration = same vector
```

This property is essential for repeatable tests.

The mock provider does not require:

- An API key
- Network access
- Model downloads
- GPU or specialized hardware
- Usage charges

### Why Not Use Python `hash()`?

Python may randomize values returned by `hash()` between processes.

A test could therefore pass in one process and produce different vectors in another.

SHA-256 provides stable output across processes and environments.

### Vector Dimension

The vector dimension is the number of values in each vector.

Example:

```text
dimension = 4
vector = [0.12, -0.50, 0.31, 0.07]
```

Every vector stored in the same vector index must use the expected dimension.

A dimension mismatch can prevent insertion or similarity comparison.

### Vector Normalization

The mock provider normalizes vectors to approximately unit length.

A normalized vector has a magnitude close to `1`.

Normalization is useful when using cosine similarity or inner-product-based search because it makes vector comparisons more consistent.

## Configuration

The provider is selected through environment configuration:

```text
EMBEDDING_PROVIDER="mock"
EMBEDDING_DIMENSION=8
```

Unit tests and the current development environment use the mock provider.

Future environments may use values such as:

```text
EMBEDDING_PROVIDER="sentence_transformers"
```

or:

```text
EMBEDDING_PROVIDER="openai"
```

Application services should not need to change when the configured provider changes.

## Why Use a Factory?

The embedding factory is the application’s provider composition point.

It:

1. Reads configuration.
2. Selects the requested provider.
3. Constructs the provider.
4. Returns it through the common interface.

This keeps provider-selection logic out of document and retrieval services.

## Testing Strategy

The tests verify that:

- The configured dimension is respected.
- The same text produces the same vector.
- Multiple texts can be embedded in one batch.
- Generated vectors are normalized.
- Blank input is rejected.
- Invalid dimensions are rejected.
- The factory returns the configured provider.
- Unknown provider names fail clearly.

Unit tests should continue using the mock provider even after a real provider is added.

Tests against real models or external APIs should be maintained separately as integration tests.

## Why Not Use a Real Model in Every Test?

Real embedding models introduce variables unrelated to application correctness:

- Model downloads
- Network failures
- API credentials
- Usage costs
- Rate limits
- Model latency
- Provider outages
- Model version changes

Unit tests should verify our logic rather than the availability of an external service.

## Production Evolution

After the foundation is complete, the project will add a proper semantic embedding provider.

The provider will be selected using:

- Retrieval quality
- Latency
- Vector dimensions
- Memory requirements
- Model size
- Licensing
- Operational cost
- Hardware requirements
- Supported languages
- AWS deployment compatibility

A local open-source model from the Sentence Transformers ecosystem is a likely development option because it can be tested without per-request fees.

A hosted provider can be selected for production if its quality and operational characteristics are preferable.

## Model Versioning

Stored vectors must be associated with information such as:

- Provider
- Model name
- Model version
- Vector dimension
- Creation time

Vectors from different embedding models should generally not be mixed in the same similarity index.

When changing the model, existing document chunks normally need to be re-embedded.

## What Would Break Without This Component?

Without the embedding abstraction:

- Business logic would depend directly on a vendor SDK.
- Unit tests could require network access.
- Changing models would require service-layer rewrites.
- Provider configuration would spread across the codebase.
- Failure handling would become inconsistent.
- Comparing multiple embedding models would be harder.

## How Would This Evolve at 10x Traffic?

At higher traffic, the system may add:

- Larger embedding batches
- Background embedding jobs
- Queue-based ingestion
- Provider rate-limit handling
- Retries with exponential backoff
- Embedding result caching
- Idempotent ingestion
- Concurrency limits
- Provider latency metrics
- Cost and token tracking
- Dead-letter queues for failed jobs

Embedding generation would likely move out of the synchronous document-upload request and into a background worker.

## Common Mistakes

- Using Python `hash()` for deterministic vectors
- Assuming mock vectors understand semantic meaning
- Mixing vectors from different models
- Changing vector dimensions without a migration
- Embedding one chunk per network request
- Running real provider calls in unit tests
- Failing to record the embedding model version
- Forgetting to re-embed documents after changing models
- Using one model for documents and another for questions

## Alternative Approaches

### Chroma Default Embedding Function

Chroma can automatically generate embeddings using a default local Sentence Transformers model.

This is convenient for prototypes but couples embedding generation more closely to the vector store.

### Direct OpenAI Integration

Application services could call OpenAI directly.

This is simple initially but increases vendor coupling and complicates unit testing.

### LangChain Embedding Interface

LangChain provides common embedding interfaces for many providers.

This can reduce integration work, but it adds a framework dependency to a foundational application boundary.

Our custom interface is intentionally small and easy to understand.

### Local Sentence Transformers

The application can load and execute an open-source model locally.

This avoids per-request API costs but introduces model downloads, memory usage, startup latency, and deployment considerations.

## Interview Questions

### 1. What is an embedding?

An embedding is a numerical representation of data. Semantically similar inputs should be located near each other in vector space.

### 2. How is an embedding model different from an LLM?

An embedding model returns vectors intended for comparison and retrieval. An LLM generates or transforms natural language and other content.

### 3. Why introduce an embedding provider abstraction?

It separates application logic from a specific vendor, improves testability, and allows providers to be changed through configuration.

### 4. Why is the mock provider deterministic?

Deterministic output makes tests repeatable. The same input must produce the same expected behavior across test runs.

### 5. Why should embedding requests be batched?

Batching reduces network overhead, improves throughput, and can help control cost and rate-limit usage.

### 6. Why must vectors have a consistent dimension?

Vector databases compare corresponding vector components. Different dimensions cannot be directly compared in the same index.

### 7. Why should document and query embeddings use the same model?

Vectors are only meaningfully comparable when they belong to the same embedding space.

### 8. What happens when the embedding model changes?

The new model creates a different vector space. Existing chunks usually need to be re-embedded and the vector index rebuilt or migrated.

### 9. Why not use a real model in unit tests?

It would make tests slower, less deterministic, more expensive, and dependent on credentials, network access, and provider availability.

### 10. What is cosine similarity?

Cosine similarity measures the angle between two vectors. It compares their direction rather than primarily comparing their magnitude.

### 11. What metadata should accompany an embedding?

Useful metadata includes model name, model version, provider, vector dimension, source document, chunk identifier, and creation timestamp.

### 12. How would you evaluate an embedding model?

Use a representative retrieval dataset and measure metrics such as recall at K, precision at K, mean reciprocal rank, latency, cost, and memory usage.

## Key Takeaway

The mock provider is temporary, but the abstraction is permanent.

It establishes a stable boundary between the application and the system responsible for turning text into vectors.