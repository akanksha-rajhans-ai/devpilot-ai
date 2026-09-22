import pytest

from app.core.config import Settings
from app.embeddings.mock_provider import MockEmbeddingProvider
from app.llm.mock_provider import MockLLMProvider
from app.rag.document_store import InMemoryDocumentStore
from app.schemas.document import DocumentIngestRequest
from app.services.document_service import DocumentService
from app.services.rag_service import RAGService


@pytest.mark.asyncio
async def test_rag_answer_contains_ranked_citations():
    store = InMemoryDocumentStore()
    settings = Settings(
        embedding_dimension=16,
        embedding_model="mock-lexical-v1",
        rag_min_similarity=-1.0,
    )
    embeddings = MockEmbeddingProvider(dimension=16)
    document = await DocumentService(
        store,
        embedding_provider=embeddings,
        settings=settings,
    ).ingest_document(
        DocumentIngestRequest(
            title="Retry Standard",
            content="Transient provider failures use bounded exponential retries.",
        )
    )

    result = await RAGService(
        store,
        embedding_provider=embeddings,
        llm_provider=MockLLMProvider(),
        settings=settings,
    ).answer("How do provider retries work?", top_k=3)

    assert result.retrieval_count == 1
    assert result.citations[0].document_id == document.document_id
    assert result.citations[0].citation_id == "S1"
    assert "Retry Standard" in result.answer
    assert result.prompt_id == "rag.answer:v1"


@pytest.mark.asyncio
async def test_rag_handles_empty_knowledge_base():
    store = InMemoryDocumentStore()
    result = await RAGService(
        store,
        embedding_provider=MockEmbeddingProvider(),
        llm_provider=MockLLMProvider(),
    ).answer("What is our architecture?")

    assert result.retrieval_count == 0
    assert result.citations == []
    assert "No relevant knowledge was retrieved" in result.answer
