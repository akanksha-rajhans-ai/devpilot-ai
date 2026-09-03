from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app, raise_server_exceptions=False)


def test_chat_returns_502_when_provider_fails():
    response = client.post(
        "/api/v1/chat",
        json={
            "message": "__simulate_provider_failure__",
            "conversation_id": "failure-test",
        },
    )

    assert response.status_code == 502

    body = response.json()
    assert body["error"]["code"] == "LLM_PROVIDER_ERROR"
    assert body["error"]["message"] == "AI provider is temporarily unavailable"
    assert body["error"]["details"]["path"] == "/api/v1/chat"
    assert body["error"]["details"]["provider"] == "mock"
    assert body["error"]["details"]["model"] == "mock-dev-model"