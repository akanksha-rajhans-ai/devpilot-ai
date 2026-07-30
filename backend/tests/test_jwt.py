from datetime import timedelta

import pytest

from app.core.security import create_access_token, decode_access_token


def test_create_and_decode_access_token():
    token = create_access_token(subject="user-123")

    payload = decode_access_token(token)

    assert payload["sub"] == "user-123"
    assert "exp" in payload


def test_access_token_supports_additional_claims():
    token = create_access_token(
        subject="user-123",
        additional_claims={"role": "admin"},
    )

    payload = decode_access_token(token)

    assert payload["sub"] == "user-123"
    assert payload["role"] == "admin"


def test_invalid_access_token_raises_value_error():
    with pytest.raises(ValueError):
        decode_access_token("not-a-real-token")


def test_expired_access_token_raises_value_error():
    token = create_access_token(
        subject="user-123",
        expires_delta=timedelta(seconds=-1),
    )

    with pytest.raises(ValueError):
        decode_access_token(token)