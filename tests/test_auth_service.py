"""
test_auth_service.py
--------------------
Tests for AuthService.
"""

import uuid

import pytest

from services.auth_service import AuthService
from repositories.user_repository import UserRepository


# ============================================================
# Password Tests
# ============================================================

def test_hash_password():
    """Test password hashing."""

    password = "password123"

    hashed = AuthService.hash_password(
        password
    )

    assert hashed != password
    assert len(hashed) == 64


def test_same_password_same_hash():
    """Test deterministic password hashing."""

    password = "password123"

    hash_one = AuthService.hash_password(
        password
    )

    hash_two = AuthService.hash_password(
        password
    )

    assert hash_one == hash_two


def test_verify_correct_password():
    """Test correct password verification."""

    password = "password123"

    hashed = AuthService.hash_password(
        password
    )

    assert AuthService.verify_password(
        password,
        hashed
    ) is True


def test_verify_wrong_password():
    """Test incorrect password verification."""

    password = "password123"

    hashed = AuthService.hash_password(
        password
    )

    assert AuthService.verify_password(
        "wrongpassword",
        hashed
    ) is False


def test_hash_empty_password():
    """Test hashing an empty password."""

    with pytest.raises(ValueError):
        AuthService.hash_password("")


# ============================================================
# Validation Tests
# ============================================================

def test_valid_email():
    """Test valid email."""

    AuthService.validate_email(
        "user@example.com"
    )


def test_invalid_email():
    """Test invalid email."""

    with pytest.raises(ValueError):
        AuthService.validate_email(
            "invalid-email"
        )


def test_empty_email():
    """Test empty email."""

    with pytest.raises(ValueError):
        AuthService.validate_email("")


def test_valid_password():
    """Test valid password."""

    AuthService.validate_password(
        "password123"
    )


def test_short_password():
    """Test short password."""

    with pytest.raises(ValueError):
        AuthService.validate_password(
            "123"
        )


# ============================================================
# Registration Tests
# ============================================================

def test_register_user():
    """Test registering a new customer."""

    email = (
        f"auth_test_{uuid.uuid4().hex[:10]}"
        "@pycommerce.test"
    )

    user = AuthService.register(
        name="Authentication Test",
        email=email,
        password="TestPassword123",
        phone="9999999999",
        address="Test Address"
    )

    assert user is not None
    assert user.user_id is not None
    assert user.email == email
    assert user.role == "customer"

    # Password must be hashed.
    assert user.password != "TestPassword123"
    assert len(user.password) == 64

    # Cleanup.
    UserRepository.delete(
        user.user_id
    )


def test_register_duplicate_email():
    """Test that duplicate email registration fails."""

    email = (
        f"duplicate_test_{uuid.uuid4().hex[:10]}"
        "@pycommerce.test"
    )

    first_user = AuthService.register(
        name="First User",
        email=email,
        password="TestPassword123"
    )

    assert first_user is not None

    try:
        with pytest.raises(ValueError):
            AuthService.register(
                name="Second User",
                email=email,
                password="TestPassword123"
            )

    finally:
        UserRepository.delete(
            first_user.user_id
        )


def test_register_invalid_password():
    """Test registration with invalid password."""

    email = (
        f"invalid_password_{uuid.uuid4().hex[:10]}"
        "@pycommerce.test"
    )

    with pytest.raises(ValueError):
        AuthService.register(
            name="Test User",
            email=email,
            password="123"
        )


def test_register_invalid_email():
    """Test registration with invalid email."""

    with pytest.raises(ValueError):
        AuthService.register(
            name="Test User",
            email="invalid-email",
            password="password123"
        )


# ============================================================
# Login Tests
# ============================================================

def test_login_success():
    """Test successful login."""

    email = (
        f"login_test_{uuid.uuid4().hex[:10]}"
        "@pycommerce.test"
    )

    password = "TestPassword123"

    user = AuthService.register(
        name="Login Test User",
        email=email,
        password=password
    )

    assert user is not None

    try:
        logged_in_user = AuthService.login(
            email=email,
            password=password
        )

        assert logged_in_user is not None
        assert logged_in_user.user_id == (
            user.user_id
        )
        assert logged_in_user.email == email

    finally:
        UserRepository.delete(
            user.user_id
        )


def test_login_wrong_password():
    """Test login with wrong password."""

    email = (
        f"wrong_password_{uuid.uuid4().hex[:10]}"
        "@pycommerce.test"
    )

    user = AuthService.register(
        name="Wrong Password User",
        email=email,
        password="CorrectPassword123"
    )

    assert user is not None

    try:
        logged_in_user = AuthService.login(
            email=email,
            password="WrongPassword123"
        )

        assert logged_in_user is None

    finally:
        UserRepository.delete(
            user.user_id
        )


def test_login_nonexistent_user():
    """Test login for an email that does not exist."""

    email = (
        f"nonexistent_{uuid.uuid4().hex[:10]}"
        "@pycommerce.test"
    )

    result = AuthService.login(
        email=email,
        password="password123"
    )

    assert result is None


# ============================================================
# Role Tests
# ============================================================

def test_customer_role():
    """Test customer role."""

    email = (
        f"customer_{uuid.uuid4().hex[:10]}"
        "@pycommerce.test"
    )

    user = AuthService.register(
        name="Customer Test",
        email=email,
        password="password123"
    )

    assert user is not None

    try:
        assert AuthService.is_customer(
            user
        ) is True

        assert AuthService.is_admin(
            user
        ) is False

    finally:
        UserRepository.delete(
            user.user_id
        )


def test_none_user_role_checks():
    """Test role checks with no user."""

    assert AuthService.is_customer(
        None
    ) is False

    assert AuthService.is_admin(
        None
    ) is False