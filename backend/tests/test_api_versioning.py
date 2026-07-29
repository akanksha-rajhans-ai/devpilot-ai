from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_api_v1_status():
    response = client.get("/api/v1/status")

    assert response.status_code == 200

    body = response.json()
    assert body["status"] == "ok"
    assert body["api_version"] == "v1"


def test_health_routes_remain_unversioned():
    response = client.get("/health/live")

    assert response.status_code == 200


def test_health_routes_are_not_under_api_v1():
    response = client.get("/api/v1/health/live")

    assert response.status_code == 404