import pytest
from sqlalchemy.orm import sessionmaker

from app.core.config import Settings
from app.db.base import Base
from app.embeddings.mock_provider import MockEmbeddingProvider
from app.rag.repository import SQLAlchemyDocumentRepository
from app.schemas.document import DocumentIngestRequest
from app.services.document_service import DocumentService
from app.db.session import create_database_engine


@pytest.mark.asyncio
async def test_sqlalchemy_repository_persists_and_searches_documents(tmp_path):
    engine = create_database_engine(f"sqlite:///{tmp_path / 'rag.db'}")
    Base.metadata.create_all(engine)
    SessionFactory = sessionmaker(bind=engine, expire_on_commit=False)
    settings = Settings(embedding_dimension=8, rag_min_similarity=-1.0)
    embeddings = MockEmbeddingProvider(dimension=8)

    with SessionFactory() as session:
        repository = SQLAlchemyDocumentRepository(session)
        ingested = await DocumentService(
            repository,
            embedding_provider=embeddings,
            settings=settings,
        ).ingest_document(
            DocumentIngestRequest(
                title="Architecture",
                content="DevPilot uses LangGraph for orchestration.",
            )
        )
        session.commit()

    with SessionFactory() as session:
        repository = SQLAlchemyDocumentRepository(session)
        stored = repository.get_document(ingested.document_id)
        query = (await embeddings.embed(["LangGraph orchestration"]))[0]
        matches = repository.search_chunks(query, limit=3, min_similarity=-1.0)

        assert stored is not None
        assert stored.title == "Architecture"
        assert matches[0].chunk.document_id == ingested.document_id

    engine.dispose()
