from fastapi.testclient import TestClient

from app.core.config import Settings
from app.core.dependencies import get_app_settings
from app.main import app

client = TestClient(app)


def test_liveness_check():
    response = client.get("/health/live")

    assert response.status_code == 200

    body = response.json()
    assert body["status"] == "alive"
    assert body["service"] == "DevPilot AI"


def test_readiness_check():
    response = client.get("/health/ready")

    assert response.status_code == 200

    body = response.json()
    assert body["status"] == "ready"
    assert body["service"] == "DevPilot AI"
    assert body["checks"]["configuration"] == "ok"


def test_liveness_check_uses_injected_settings():
    def override_settings():
        return Settings(
            app_name="TestPilot",
            app_version="9.9.9",
            environment="test",
        )

    app.dependency_overrides[get_app_settings] = override_settings

    response = client.get("/health/live")

    app.dependency_overrides.clear()

    assert response.status_code == 200

    body = response.json()
    assert body["service"] == "TestPilot"
    assert body["version"] == "9.9.9"
    assert body["environment"] == "test"