from fastapi.testclient import TestClient

from app.main import app
from app.rag.document_store import document_store

client = TestClient(app)


def test_document_ingestion_stores_document():
    document_store.clear()

    response = client.post(
        "/api/v1/documents",
        json={
            "title": "RAG Notes",
            "content": "Retrieval augmented generation combines search with generation.",
        },
    )

    assert response.status_code == 200

    body = response.json()
    assert body["document_id"]
    assert body["title"] == "RAG Notes"
    assert body["status"] == "ingested"

    stored = document_store.get_document(body["document_id"])
    assert stored is not None
    assert stored.title == "RAG Notes"
    assert stored.content == "Retrieval augmented generation combines search with generation."


def test_document_ingestion_requires_content():
    response = client.post(
        "/api/v1/documents",
        json={
            "title": "Empty Doc",
            "content": "",
        },
    )

    assert response.status_code == 422

    body = response.json()

    assert body["chunk_count"] >= 1

    chunks = document_store.get_chunks(body["document_id"])

    assert len(chunks) == body["chunk_count"]
    assert chunks[0].document_id == body["document_id"]
    assert chunks[0].chunk_index == 0