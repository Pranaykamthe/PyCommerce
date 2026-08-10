"""
Tests for UserService.
"""

import pytest

from unittest.mock import patch
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


# ============================================================
# UserService Business Logic Tests
# ============================================================

def test_create_user():
    """Test creating a user through UserService."""

    user = User(
        name="  Pranay  ",
        email="  PRANAY@EXAMPLE.COM  ",
        password="password123",
        phone=" 9999999999 ",
        address=" Pune ",
        role="customer"
    )

    with patch(
        "services.user_service.AuthService.hash_password",
        return_value="hashed_password"
    ) as mock_hash, patch(
        "services.user_service.UserRepository.create",
        return_value=user
    ) as mock_create:

        result = UserService.create_user(user)

    assert result is user

    assert user.name == "Pranay"
    assert user.email == "pranay@example.com"
    assert user.phone == "9999999999"
    assert user.address == "Pune"
    assert user.password == "hashed_password"

    mock_hash.assert_called_once_with(
        "password123"
    )

    mock_create.assert_called_once_with(
        user
    )


def test_get_user():
    """Test retrieving a user by ID."""

    user = User(
        user_id=1,
        name="Pranay",
        email="pranay@example.com",
        password="hashed_password",
        phone="9999999999",
        address="Pune",
        role="customer"
    )

    with patch(
        "services.user_service.UserRepository.get_by_id",
        return_value=user
    ) as mock_get:

        result = UserService.get_user(1)

    assert result is user

    mock_get.assert_called_once_with(1)


def test_get_user_by_email():
    """Test retrieving a user by email."""

    user = User(
        user_id=1,
        name="Pranay",
        email="pranay@example.com",
        password="hashed_password",
        phone="9999999999",
        address="Pune",
        role="customer"
    )

    with patch(
        "services.user_service.UserRepository.get_by_email",
        return_value=user
    ) as mock_get:

        result = UserService.get_user_by_email(
            "  PRANAY@EXAMPLE.COM  "
        )

    assert result is user

    mock_get.assert_called_once_with(
        "pranay@example.com"
    )


def test_get_all_users():
    """Test retrieving all active users."""

    users = [
        User(
            user_id=1,
            name="Pranay",
            email="pranay@example.com",
            password="hashed_password",
            phone="9999999999",
            address="Pune",
            role="customer"
        ),
        User(
            user_id=2,
            name="Admin",
            email="admin@example.com",
            password="hashed_password",
            phone="8888888888",
            address="Mumbai",
            role="admin"
        )
    ]

    with patch(
        "services.user_service.UserRepository.get_all",
        return_value=users
    ) as mock_get:

        result = UserService.get_all_users()

    assert result == users

    mock_get.assert_called_once_with()


def test_update_user():
    """Test updating an existing user."""

    user = User(
        user_id=1,
        name="  Updated User  ",
        email="  UPDATED@EXAMPLE.COM  ",
        password="hashed_password",
        phone=" 8888888888 ",
        address=" Mumbai ",
        role="customer"
    )

    with patch(
        "services.user_service.UserRepository.update",
        return_value=True
    ) as mock_update:

        result = UserService.update_user(user)

    assert result is True

    assert user.name == "Updated User"
    assert user.email == "updated@example.com"
    assert user.phone == "8888888888"
    assert user.address == "Mumbai"
    assert user.password == "hashed_password"

    mock_update.assert_called_once_with(
        user
    )


def test_delete_user():
    """Test deleting a user through UserService."""

    with patch(
        "services.user_service.UserRepository.delete",
        return_value=True
    ) as mock_delete:

        result = UserService.delete_user(1)

    assert result is True

    mock_delete.assert_called_once_with(1)

def test_update_user_without_password():
    """Test updating a user without a password hash."""

    user = User(
        user_id=1,
        name="Test User",
        email="test@example.com",
        password="",
        phone="",
        address="",
        role="customer"
    )

    with pytest.raises(ValueError):
        UserService.update_user(user)