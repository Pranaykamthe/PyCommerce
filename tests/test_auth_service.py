import pytest

from services.auth_service import AuthService


def test_hash_password():
    password = "password123"

    hashed = AuthService.hash_password(password)

    assert hashed != password
    assert len(hashed) == 64


def test_same_password_same_hash():
    password = "password123"

    hash1 = AuthService.hash_password(password)
    hash2 = AuthService.hash_password(password)

    assert hash1 == hash2


def test_different_password_different_hash():
    hash1 = AuthService.hash_password(
        "password123"
    )

    hash2 = AuthService.hash_password(
        "password456"
    )

    assert hash1 != hash2


def test_empty_password():
    with pytest.raises(ValueError):
        AuthService.hash_password("")


def test_verify_correct_password():
    password = "password123"

    hashed_password = AuthService.hash_password(
        password
    )

    assert AuthService.verify_password(
        password,
        hashed_password
    ) is True


def test_verify_wrong_password():
    password = "password123"

    hashed_password = AuthService.hash_password(
        password
    )

    assert AuthService.verify_password(
        "wrongpassword",
        hashed_password
    ) is False


def test_verify_empty_password():
    hashed_password = AuthService.hash_password(
        "password123"
    )

    assert AuthService.verify_password(
        "",
        hashed_password
    ) is False