"""
Tests for CategoryService.
"""

import pytest

from models.category import Category
from services.category_service import CategoryService


# ============================================================
# Category Validation Tests
# ============================================================

def test_validate_category():
    """Test valid category information."""

    CategoryService.validate_category(
        name="Electronics",
        description="Electronic products"
    )


def test_empty_category_name():
    """Test empty category name."""

    with pytest.raises(ValueError):

        CategoryService.validate_category(
            name="",
            description="Electronics"
        )


def test_whitespace_category_name():
    """Test whitespace-only category name."""

    with pytest.raises(ValueError):

        CategoryService.validate_category(
            name="   ",
            description="Electronics"
        )


# ============================================================
# Create Category Tests
# ============================================================

def test_create_category_validation():
    """
    Test category creation validation.

    This test validates the model without requiring MySQL.
    """

    category = Category(
        name="Electronics",
        description="Electronic products"
    )

    CategoryService.validate_category(
        name=category.name,
        description=category.description
    )


def test_create_category_invalid_name():
    """Test category creation with invalid name."""

    category = Category(
        name="",
        description="Invalid category"
    )

    with pytest.raises(ValueError):

        CategoryService.create_category(
            category
        )


# ============================================================
# Get Category Tests
# ============================================================

def test_get_category_invalid_id():
    """Test getting a category with invalid ID."""

    with pytest.raises(ValueError):

        CategoryService.get_category(
            0
        )


def test_get_category_negative_id():
    """Test getting a category with negative ID."""

    with pytest.raises(ValueError):

        CategoryService.get_category(
            -1
        )


# ============================================================
# Get All Categories Tests
# ============================================================

def test_get_all_categories():
    """Test retrieving all active categories."""

    categories = (
        CategoryService.get_all_categories()
    )

    assert isinstance(
        categories,
        list
    )


# ============================================================
# Update Category Tests
# ============================================================

def test_update_category_without_id():
    """Test updating a category without an ID."""

    category = Category(
        category_id=None,
        name="Electronics",
        description="Updated description"
    )

    with pytest.raises(ValueError):

        CategoryService.update_category(
            category
        )


def test_update_category_invalid_name():
    """Test updating a category with an invalid name."""

    category = Category(
        category_id=1,
        name="",
        description="Updated description"
    )

    with pytest.raises(ValueError):

        CategoryService.update_category(
            category
        )


# ============================================================
# Delete Category Tests
# ============================================================

def test_delete_category_invalid_id():
    """Test deleting a category with invalid ID."""

    with pytest.raises(ValueError):

        CategoryService.delete_category(
            0
        )


def test_delete_category_negative_id():
    """Test deleting a category with negative ID."""

    with pytest.raises(ValueError):

        CategoryService.delete_category(
            -1
        )