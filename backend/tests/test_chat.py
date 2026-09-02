from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_chat_returns_mock_response():
    response = client.post(
        "/api/v1/chat",
        json={
            "message": "Explain RAG in simple terms",
            "conversation_id": "demo-1",
        },
    )

    assert response.status_code == 200

    body = response.json()
    assert "Mock response to:" in body["answer"]
    assert "Explain RAG in simple terms" in body["answer"]
    assert body["provider"] == "mock"
    assert body["model"] == "mock-dev-model"
    assert body["prompt_id"] == "chat.general:v1"
    assert body["conversation_id"] == "demo-1"
    assert body["latency_ms"] >= 0
    assert body["usage"]["input_tokens"] is not None
    assert body["usage"]["output_tokens"] is not None
    assert body["usage"]["total_tokens"] is not None


def test_chat_requires_non_empty_message():
    response = client.post(
        "/api/v1/chat",
        json={
            "message": "",
        },
    )

    assert response.status_code == 422

    body = response.json()
    assert body["error"]["code"] == "VALIDATION_ERROR"