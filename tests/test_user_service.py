import pytest

from services.user_service import UserService


def test_valid_username():
    UserService.validate_username("pranay")


def test_empty_username():
    with pytest.raises(ValueError):
        UserService.validate_username("")


def test_short_username():
    with pytest.raises(ValueError):
        UserService.validate_username("ab")


def test_valid_email():
    UserService.validate_email("user@example.com")


def test_empty_email():
    with pytest.raises(ValueError):
        UserService.validate_email("")


def test_invalid_email():
    with pytest.raises(ValueError):
        UserService.validate_email("userexample.com")


def test_valid_password():
    UserService.validate_password("password123")


def test_empty_password():
    with pytest.raises(ValueError):
        UserService.validate_password("")


def test_short_password():
    with pytest.raises(ValueError):
        UserService.validate_password("123")


def test_valid_user():
    UserService.validate_user(
        username="pranay",
        email="pranay@example.com",
        password="password123"
    )