from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app, raise_server_exceptions=False)


def test_not_found_error_shape():
    response = client.get("/missing-route")

    assert response.status_code == 404

    body = response.json()
    assert body["error"]["code"] == "NOT_FOUND"
    assert body["error"]["message"] == "Resource not found"
    assert body["error"]["details"]["path"] == "/missing-route"


def test_validation_error_shape():
    response = client.get("/__test__/validation")

    assert response.status_code == 422

    body = response.json()
    assert body["error"]["code"] == "VALIDATION_ERROR"
    assert body["error"]["message"] == "Request validation failed"
    assert body["error"]["details"]["path"] == "/__test__/validation"
    assert "errors" in body["error"]["details"]


def test_internal_server_error_shape():
    response = client.get("/__test__/error")

    assert response.status_code == 500

    body = response.json()
    assert body["error"]["code"] == "INTERNAL_SERVER_ERROR"
    assert body["error"]["message"] == "An unexpected error occurred"
    assert body["error"]["details"]["path"] == "/__test__/error"