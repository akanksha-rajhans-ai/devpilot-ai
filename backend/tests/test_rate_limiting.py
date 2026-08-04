from collections import defaultdict, deque

from fastapi.testclient import TestClient

from app.core.config import Settings
from app.main import app


def set_test_settings(settings: Settings) -> None:
    app.state.settings_override = settings
    app.state.rate_limit_store = defaultdict(deque)


def clear_test_settings() -> None:
    if hasattr(app.state, "settings_override"):
        del app.state.settings_override

    if hasattr(app.state, "rate_limit_store"):
        del app.state.rate_limit_store


def test_rate_limit_headers_are_added():
    set_test_settings(
        Settings(
            rate_limit_enabled=True,
            rate_limit_requests=10,
            rate_limit_window_seconds=60,
        )
    )

    client = TestClient(app)
    response = client.get("/health/live")

    clear_test_settings()

    assert response.status_code == 200
    assert response.headers["X-RateLimit-Limit"] == "10"
    assert "X-RateLimit-Remaining" in response.headers


def test_rate_limit_blocks_after_limit():
    set_test_settings(
        Settings(
            rate_limit_enabled=True,
            rate_limit_requests=1,
            rate_limit_window_seconds=60,
        )
    )

    client = TestClient(app)
    first_response = client.get("/health/live")
    second_response = client.get("/health/live")

    clear_test_settings()

    assert first_response.status_code == 200
    assert second_response.status_code == 429

    body = second_response.json()
    assert body["error"]["code"] == "RATE_LIMIT_EXCEEDED"
    assert body["error"]["message"] == "Too many requests"


def test_rate_limit_can_be_disabled():
    set_test_settings(
        Settings(
            rate_limit_enabled=False,
            rate_limit_requests=1,
            rate_limit_window_seconds=60,
        )
    )

    client = TestClient(app)
    first_response = client.get("/health/live")
    second_response = client.get("/health/live")

    clear_test_settings()

    assert first_response.status_code == 200
    assert second_response.status_code == 200