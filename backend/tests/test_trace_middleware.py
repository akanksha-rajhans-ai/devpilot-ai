from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app, raise_server_exceptions=False)


def test_trace_id_header_is_added():
    response = client.get("/health/live")

    assert response.status_code == 200
    assert "X-Trace-Id" in response.headers
    assert response.headers["X-Trace-Id"]


def test_existing_trace_id_is_preserved():
    response = client.get(
        "/health/live",
        headers={"X-Trace-Id": "test-trace-123"},
    )

    assert response.status_code == 200
    assert response.headers["X-Trace-Id"] == "test-trace-123"


def test_error_response_includes_trace_id():
    response = client.get(
        "/missing-route",
        headers={"X-Trace-Id": "missing-route-trace"},
    )

    assert response.status_code == 404

    body = response.json()
    assert body["error"]["trace_id"] == "missing-route-trace"