"""
test_user_repository.py
-----------------------
Integration tests for UserRepository.

These tests interact with the MySQL database.
"""

import uuid

from models.user import User
from repositories.user_repository import UserRepository
from services.auth_service import AuthService


def create_test_user() -> User:
    """Create a unique test user."""

    unique_email = (
        f"test_{uuid.uuid4().hex[:10]}"
        "@pycommerce.test"
    )

    return User(
        name="PyCommerce Test User",
        email=unique_email,
        password=AuthService.hash_password(
            "TestPassword123"
        ),
        phone="9999999999",
        address="Test Address",
        role="customer"
    )


def test_create_user():
    """Test creating a user."""

    user = create_test_user()

    created_user = UserRepository.create(user)

    assert created_user is not None
    assert created_user.user_id is not None
    assert created_user.email == user.email

    # Verify user can be retrieved.
    saved_user = UserRepository.get_by_id(
        created_user.user_id
    )

    assert saved_user is not None
    assert saved_user.user_id == created_user.user_id
    assert saved_user.name == "PyCommerce Test User"
    assert saved_user.email == created_user.email
    assert saved_user.role == "customer"

    # Clean up.
    UserRepository.delete(
        created_user.user_id
    )


def test_get_user_by_id():
    """Test retrieving a user by ID."""

    user = create_test_user()

    created_user = UserRepository.create(user)

    assert created_user is not None
    assert created_user.user_id is not None

    user_id = created_user.user_id

    retrieved_user = UserRepository.get_by_id(
        user_id
    )

    assert retrieved_user is not None
    assert retrieved_user.user_id == user_id
    assert retrieved_user.email == user.email

    UserRepository.delete(user_id)


def test_get_user_by_email():
    """Test retrieving a user by email."""

    user = create_test_user()

    created_user = UserRepository.create(user)

    assert created_user is not None

    retrieved_user = UserRepository.get_by_email(
        user.email
    )

    assert retrieved_user is not None
    assert retrieved_user.email == user.email
    assert retrieved_user.name == user.name

    UserRepository.delete(
        created_user.user_id
    )


def test_get_user_not_found():
    """Test retrieving a nonexistent user."""

    user = UserRepository.get_by_id(
        999999999
    )

    assert user is None


def test_get_all_users():
    """Test retrieving all active users."""

    users = UserRepository.get_all()

    assert isinstance(users, list)


def test_update_user():
    """Test updating a user."""

    user = create_test_user()

    created_user = UserRepository.create(user)

    assert created_user is not None
    assert created_user.user_id is not None

    created_user.name = "Updated Test User"
    created_user.phone = "8888888888"
    created_user.address = "Updated Address"

    result = UserRepository.update(
        created_user
    )

    assert result is True

    updated_user = UserRepository.get_by_id(
        created_user.user_id
    )

    assert updated_user is not None
    assert updated_user.name == "Updated Test User"
    assert updated_user.phone == "8888888888"
    assert updated_user.address == "Updated Address"

    UserRepository.delete(
        created_user.user_id
    )


def test_update_user_without_id():
    """Test updating a user without an ID."""

    user = create_test_user()

    result = UserRepository.update(user)

    assert result is False


def test_delete_user():
    """Test soft deleting a user."""

    user = create_test_user()

    created_user = UserRepository.create(user)

    assert created_user is not None
    assert created_user.user_id is not None

    user_id = created_user.user_id

    result = UserRepository.delete(user_id)

    assert result is True

    # Soft-deleted users should not be returned.
    deleted_user = UserRepository.get_by_id(
        user_id
    )

    assert deleted_user is None


def test_delete_user_not_found():
    """Test deleting a nonexistent user."""

    result = UserRepository.delete(
        999999999
    )

    assert result is False