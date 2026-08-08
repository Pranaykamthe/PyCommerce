"""
test_user_model.py
------------------
Tests for the User model.
"""

from models.user import User


def test_create_user():
    """Test creating a user."""

    user = User(
        user_id=1,
        name="Test User",
        email="test@example.com",
        password="password123",
        phone="9876543210",
        address="Pune",
    )

    assert user.user_id == 1
    assert user.name == "Test User"
    assert user.email == "test@example.com"
    assert user.password == "password123"
    assert user.phone == "9876543210"
    assert user.address == "Pune"
    assert user.role == "customer"


def test_create_admin():
    """Test creating an admin user."""

    admin = User(
        user_id=2,
        name="Admin",
        email="admin@pycommerce.com",
        password="admin123",
        role="admin",
    )

    assert admin.role == "admin"


def test_user_string():
    """Test User string representation."""

    user = User(
        user_id=1,
        name="Test User",
        email="test@example.com",
    )

    result = str(user)

    assert "Test User" in result
    assert "test@example.com" in result