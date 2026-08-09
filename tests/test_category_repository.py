"""
Integration tests for CategoryRepository.

These tests interact with the MySQL database.
"""

import uuid

from models.category import Category
from repositories.category_repository import CategoryRepository


# ============================================================
# Create Category
# ============================================================

def test_create_category():
    """Test creating a category in MySQL."""

    category_name = (
        f"Test Category PyCommerce "
        f"{uuid.uuid4().hex[:8]}"
    )

    category = Category(
        name=category_name,
        description="Temporary test category"
    )

    created_category = (
        CategoryRepository.create(
            category
        )
    )

    assert created_category is not None

    assert (
        created_category.category_id
        is not None
    )

    category_id = (
        created_category.category_id
    )

    saved_category = (
        CategoryRepository.get_by_id(
            category_id
        )
    )

    assert saved_category is not None

    assert (
        saved_category.category_id
        == category_id
    )

    assert (
        saved_category.name
        == category_name
    )

    assert (
        saved_category.description
        == "Temporary test category"
    )

    # Clean up.
    CategoryRepository.delete(
        category_id
    )


# ============================================================
# Get Category By ID
# ============================================================

def test_get_category_by_id():
    """Test retrieving a category by ID."""

    category_name = (
        f"Read Test Category "
        f"{uuid.uuid4().hex[:8]}"
    )

    category = Category(
        name=category_name,
        description="Category read test"
    )

    created_category = (
        CategoryRepository.create(
            category
        )
    )

    assert created_category is not None

    assert (
        created_category.category_id
        is not None
    )

    category_id = (
        created_category.category_id
    )

    retrieved_category = (
        CategoryRepository.get_by_id(
            category_id
        )
    )

    assert retrieved_category is not None

    assert (
        retrieved_category.category_id
        == category_id
    )

    assert (
        retrieved_category.name
        == category_name
    )

    assert (
        retrieved_category.description
        == "Category read test"
    )

    # Clean up.
    CategoryRepository.delete(
        category_id
    )


# ============================================================
# Get Category Not Found
# ============================================================

def test_get_category_not_found():
    """Test retrieving a category that does not exist."""

    category = (
        CategoryRepository.get_by_id(
            999999999
        )
    )

    assert category is None


# ============================================================
# Get All Categories
# ============================================================

def test_get_all_categories():
    """Test retrieving all active categories."""

    categories = (
        CategoryRepository.get_all()
    )

    assert isinstance(
        categories,
        list
    )


# ============================================================
# Update Category
# ============================================================

def test_update_category():
    """Test updating a category."""

    category_name = (
        f"Update Test Category "
        f"{uuid.uuid4().hex[:8]}"
    )

    updated_name = (
        f"Updated Test Category "
        f"{uuid.uuid4().hex[:8]}"
    )

    category = Category(
        name=category_name,
        description="Original description"
    )

    created_category = (
        CategoryRepository.create(
            category
        )
    )

    assert created_category is not None

    assert (
        created_category.category_id
        is not None
    )

    created_category.name = (
        updated_name
    )

    created_category.description = (
        "Updated description"
    )

    result = (
        CategoryRepository.update(
            created_category
        )
    )

    assert result is True

    updated_category = (
        CategoryRepository.get_by_id(
            created_category.category_id
        )
    )

    assert updated_category is not None

    assert (
        updated_category.name
        == updated_name
    )

    assert (
        updated_category.description
        == "Updated description"
    )

    # Clean up.
    CategoryRepository.delete(
        created_category.category_id
    )


# ============================================================
# Update Category Without ID
# ============================================================

def test_update_category_without_id():
    """Test updating a category without an ID."""

    category = Category(
        category_id=None,
        name="Invalid Update Category",
        description="Test"
    )

    result = (
        CategoryRepository.update(
            category
        )
    )

    assert result is False


# ============================================================
# Delete Category
# ============================================================

def test_delete_category():
    """
    Test soft-deleting a category.
    """

    category_name = (
        f"Delete Test Category "
        f"{uuid.uuid4().hex[:8]}"
    )

    category = Category(
        name=category_name,
        description="Category deletion test"
    )

    created_category = (
        CategoryRepository.create(
            category
        )
    )

    assert created_category is not None

    assert (
        created_category.category_id
        is not None
    )

    category_id = (
        created_category.category_id
    )

    result = (
        CategoryRepository.delete(
            category_id
        )
    )

    assert result is True

    # Soft-deleted categories should no
    # longer be returned by get_by_id().
    deleted_category = (
        CategoryRepository.get_by_id(
            category_id
        )
    )

    assert deleted_category is None


# ============================================================
# Delete Category Not Found
# ============================================================

def test_delete_category_not_found():
    """Test deleting a category that does not exist."""

    result = (
        CategoryRepository.delete(
            999999999
        )
    )

    assert result is False