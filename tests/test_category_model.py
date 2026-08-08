"""
test_category_model.py
----------------------
Tests for the Category model.
"""

from models.category import Category


def test_create_category():
    """Test creating a category."""

    category = Category(
        category_id=1,
        name="Electronics",
        description="Electronic products and accessories",
    )

    assert category.category_id == 1
    assert category.name == "Electronics"
    assert category.description == "Electronic products and accessories"


def test_category_default_values():
    """Test category default values."""

    category = Category()

    assert category.category_id is None
    assert category.name == ""
    assert category.description == ""
    assert category.created_at is None


def test_category_string():
    """Test Category string representation."""

    category = Category(
        category_id=1,
        name="Electronics",
    )

    result = str(category)

    assert "Electronics" in result
    assert "1" in result