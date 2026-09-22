import pytest

from app.core.config import Settings
from app.embeddings.mock_provider import MockEmbeddingProvider
from app.evaluation.rag import RetrievalCase, evaluate_retrieval
from app.rag.document_store import InMemoryDocumentStore
from app.schemas.document import DocumentIngestRequest
from app.services.document_service import DocumentService


@pytest.mark.asyncio
async def test_retrieval_evaluation_reports_hit_rate_and_mrr():
    store = InMemoryDocumentStore()
    settings = Settings(embedding_dimension=16)
    embeddings = MockEmbeddingProvider(dimension=16)
    document = await DocumentService(
        store,
        embedding_provider=embeddings,
        settings=settings,
    ).ingest_document(
        DocumentIngestRequest(
            title="Tracing",
            content="Trace IDs correlate logs across request boundaries.",
        )
    )

    result = await evaluate_retrieval(
        store,
        embeddings,
        [RetrievalCase("How do trace IDs help logs?", document.document_id)],
        top_k=1,
    )

    assert result.case_count == 1
    assert result.hit_rate_at_k == 1.0
    assert result.mean_reciprocal_rank == 1.0
    assert result.failures == []
