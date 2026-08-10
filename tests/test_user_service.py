"""
Tests for UserService.
"""

import pytest

from models.user import User
from services.auth_service import AuthService
from services.user_service import UserService


# ============================================================
# Validation Tests
# ============================================================

def test_valid_username():
    """Test a valid username."""

    UserService.validate_username(
        "Pranay"
    )


def test_empty_username():
    """Test an empty username."""

    with pytest.raises(ValueError):
        UserService.validate_username("")


def test_short_username():
    """Test a username shorter than 3 characters."""

    with pytest.raises(ValueError):
        UserService.validate_username("ab")


def test_valid_email():
    """Test a valid email."""

    UserService.validate_email(
        "user@example.com"
    )


def test_empty_email():
    """Test an empty email."""

    with pytest.raises(ValueError):
        UserService.validate_email("")


def test_invalid_email():
    """Test an invalid email."""

    with pytest.raises(ValueError):
        UserService.validate_email(
            "userexample.com"
        )


def test_valid_password():
    """Test a valid password."""

    UserService.validate_password(
        "password123"
    )


def test_empty_password():
    """Test an empty password."""

    with pytest.raises(ValueError):
        UserService.validate_password("")


def test_short_password():
    """Test a password shorter than 6 characters."""

    with pytest.raises(ValueError):
        UserService.validate_password(
            "123"
        )


def test_valid_customer_role():
    """Test customer role."""

    UserService.validate_role(
        "customer"
    )


def test_valid_admin_role():
    """Test admin role."""

    UserService.validate_role(
        "admin"
    )


def test_invalid_role():
    """Test invalid user role."""

    with pytest.raises(ValueError):
        UserService.validate_role(
            "manager"
        )


def test_valid_user():
    """Test complete valid user information."""

    UserService.validate_user(
        username="Pranay",
        email="user@example.com",
        password="password123",
        role="customer"
    )


# ============================================================
# User Object Tests
# ============================================================

def test_user_model():
    """Test creating a User model."""

    user = User(
        name="Pranay",
        email="pranay@example.com",
        password="password123",
        phone="9999999999",
        address="Pune",
        role="customer"
    )

    assert user.name == "Pranay"
    assert user.email == "pranay@example.com"
    assert user.role == "customer"


# ============================================================
# Password Hashing Tests
# ============================================================

def test_create_user_password_hash():
    """
    Test that a user's password can be hashed
    before database storage.
    """

    password = "password123"

    hashed_password = AuthService.hash_password(
        password
    )

    assert hashed_password != password

    # Password should use the new PBKDF2 format.
    assert hashed_password.startswith(
        "pbkdf2_sha256$"
    )

    # Hashed password must verify correctly.
    assert AuthService.verify_password(
        password,
        hashed_password
    ) is True


# ============================================================
# ID Validation Tests
# ============================================================

def test_get_user_invalid_id():
    """Test invalid user ID."""

    with pytest.raises(ValueError):
        UserService.get_user(0)


def test_get_user_negative_id():
    """Test negative user ID."""

    with pytest.raises(ValueError):
        UserService.get_user(-1)


def test_delete_user_invalid_id():
    """Test invalid user ID during deletion."""

    with pytest.raises(ValueError):
        UserService.delete_user(0)


def test_delete_user_negative_id():
    """Test negative user ID during deletion."""

    with pytest.raises(ValueError):
        UserService.delete_user(-1)


def test_update_user_without_id():
    """Test updating a user without a user ID."""

    user = User(
        user_id=None,
        name="Test User",
        email="test@example.com",
        password="hashed_password",
        phone="",
        address="",
        role="customer"
    )

    with pytest.raises(ValueError):
        UserService.update_user(user)