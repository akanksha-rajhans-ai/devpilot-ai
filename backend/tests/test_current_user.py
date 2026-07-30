from fastapi.testclient import TestClient

from app.core.security import create_access_token
from app.main import app

client = TestClient(app)


def test_me_requires_authentication():
    response = client.get("/api/v1/me")

    assert response.status_code == 401

    body = response.json()
    assert body["error"]["code"] == "HTTP_ERROR"
    assert body["error"]["message"] == "Authentication required"


def test_me_rejects_invalid_token():
    response = client.get(
        "/api/v1/me",
        headers={"Authorization": "Bearer not-a-real-token"},
    )

    assert response.status_code == 401

    body = response.json()
    assert body["error"]["code"] == "HTTP_ERROR"
    assert body["error"]["message"] == "Invalid or expired token"


def test_me_returns_current_user_for_valid_token():
    token = create_access_token(subject="user-123")

    response = client.get(
        "/api/v1/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200

    body = response.json()
    assert body["id"] == "user-123"