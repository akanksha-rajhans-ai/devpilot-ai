from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_chat_returns_mock_response():
    response = client.post(
        "/chat",
        json={
            "message": "Explain RAG in simple terms",
            "conversation_id": "demo-1",
        },
    )

    assert response.status_code == 200

    body = response.json()
    assert body["answer"] == "Mock response to: Explain RAG in simple terms"
    assert body["provider"] == "mock"
    assert body["model"] == "mock-dev-model"
    assert body["conversation_id"] == "demo-1"