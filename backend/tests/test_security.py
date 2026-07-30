from pydantic import ValidationError

from app.core.security import hash_password, verify_password
from app.schemas.auth import UserCreate, UserLogin, UserPublic


def test_hash_password_does_not_return_plaintext():
    password = "SuperSecret123"

    password_hash = hash_password(password)

    assert password_hash != password
    assert password not in password_hash


def test_verify_password_accepts_correct_password():
    password = "SuperSecret123"
    password_hash = hash_password(password)

    assert verify_password(password, password_hash) is True


def test_verify_password_rejects_wrong_password():
    password_hash = hash_password("SuperSecret123")

    assert verify_password("WrongPassword123", password_hash) is False


def test_user_create_requires_valid_email():
    try:
        UserCreate(email="not-an-email", password="SuperSecret123")
    except ValidationError:
        return

    raise AssertionError("Expected validation error for invalid email")


def test_user_create_requires_minimum_password_length():
    try:
        UserCreate(email="user@example.com", password="short")
    except ValidationError:
        return

    raise AssertionError("Expected validation error for short password")


def test_user_login_allows_non_empty_password():
    login = UserLogin(email="user@example.com", password="x")

    assert login.email == "user@example.com"


def test_user_public_does_not_include_password_fields():
    user = UserPublic(
        id="user-1",
        email="user@example.com",
        is_active=True,
    )

    body = user.model_dump()

    assert "password" not in body
    assert "password_hash" not in body