from fastapi.testclient import TestClient

from app.core.security import create_access_token
from app.main import app

client = TestClient(app)


def test_admin_route_requires_authentication():
    response = client.get("/api/v1/admin/status")

    assert response.status_code == 401

    body = response.json()
    assert body["error"]["message"] == "Authentication required"


def test_admin_route_rejects_user_without_admin_role():
    token = create_access_token(
        subject="user-123",
        additional_claims={"roles": ["developer"]},
    )

    response = client.get(
        "/api/v1/admin/status",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 403

    body = response.json()
    assert body["error"]["message"] == "Insufficient permissions"


def test_admin_route_allows_admin_role():
    token = create_access_token(
        subject="admin-123",
        additional_claims={"roles": ["admin"]},
    )

    response = client.get(
        "/api/v1/admin/status",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200

    body = response.json()
    assert body["status"] == "ok"
    assert body["admin"] == "admin-123"