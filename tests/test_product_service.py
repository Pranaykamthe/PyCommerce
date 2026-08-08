"""
test_product_service.py
-----------------------
Tests for ProductService.
"""

import pytest

from models.product import Product
from services.product_service import ProductService


# ============================================================
# Product Validation Tests
# ============================================================

def test_validate_product():
    """Test valid product information."""

    ProductService.validate_product(
        category_id=1,
        name="Laptop",
        price=50000,
        stock=10
    )


def test_invalid_category_id():
    """Test invalid category ID."""

    with pytest.raises(ValueError):
        ProductService.validate_product(
            category_id=0,
            name="Laptop",
            price=50000,
            stock=10
        )


def test_empty_product_name():
    """Test empty product name."""

    with pytest.raises(ValueError):
        ProductService.validate_product(
            category_id=1,
            name="",
            price=50000,
            stock=10
        )


def test_whitespace_product_name():
    """Test whitespace-only product name."""

    with pytest.raises(ValueError):
        ProductService.validate_product(
            category_id=1,
            name="   ",
            price=50000,
            stock=10
        )


def test_negative_price():
    """Test negative product price."""

    with pytest.raises(ValueError):
        ProductService.validate_product(
            category_id=1,
            name="Laptop",
            price=-100,
            stock=10
        )


def test_negative_stock():
    """Test negative product stock."""

    with pytest.raises(ValueError):
        ProductService.validate_product(
            category_id=1,
            name="Laptop",
            price=50000,
            stock=-1
        )


# ============================================================
# Product Availability Tests
# ============================================================

def test_product_available():
    """Test product with available stock."""

    product = Product(
        product_id=1,
        category_id=1,
        name="Laptop",
        description="Test laptop",
        price=50000,
        stock=10,
        image_url=""
    )

    assert ProductService.is_available(product) is True


def test_product_not_available():
    """Test product with zero stock."""

    product = Product(
        product_id=1,
        category_id=1,
        name="Laptop",
        description="Test laptop",
        price=50000,
        stock=0,
        image_url=""
    )

    assert ProductService.is_available(product) is False


# ============================================================
# Stock Increase Tests
# ============================================================

def test_increase_stock():
    """Test increasing product stock."""

    product = Product(
        product_id=1,
        category_id=1,
        name="Laptop",
        description="Test laptop",
        price=50000,
        stock=10,
        image_url=""
    )

    ProductService.increase_stock(
        product,
        5
    )

    assert product.stock == 15


def test_increase_stock_invalid_quantity():
    """Test increasing stock with invalid quantity."""

    product = Product(
        product_id=1,
        category_id=1,
        name="Laptop",
        description="Test laptop",
        price=50000,
        stock=10,
        image_url=""
    )

    with pytest.raises(ValueError):
        ProductService.increase_stock(
            product,
            0
        )


# ============================================================
# Stock Decrease Tests
# ============================================================

def test_decrease_stock():
    """Test decreasing product stock."""

    product = Product(
        product_id=1,
        category_id=1,
        name="Laptop",
        description="Test laptop",
        price=50000,
        stock=10,
        image_url=""
    )

    ProductService.decrease_stock(
        product,
        3
    )

    assert product.stock == 7


def test_decrease_stock_invalid_quantity():
    """Test decreasing stock with invalid quantity."""

    product = Product(
        product_id=1,
        category_id=1,
        name="Laptop",
        description="Test laptop",
        price=50000,
        stock=10,
        image_url=""
    )

    with pytest.raises(ValueError):
        ProductService.decrease_stock(
            product,
            0
        )


def test_decrease_stock_insufficient():
    """Test decreasing stock beyond available quantity."""

    product = Product(
        product_id=1,
        category_id=1,
        name="Laptop",
        description="Test laptop",
        price=50000,
        stock=2,
        image_url=""
    )

    with pytest.raises(ValueError):
        ProductService.decrease_stock(
            product,
            5
        )


# ============================================================
# Create Product Tests
# ============================================================

def test_create_product_validation():
    """
    Test product creation validation.

    This test does not connect to MySQL.
    """

    product = Product(
        category_id=1,
        name="Laptop",
        description="Test laptop",
        price=50000,
        stock=10,
        image_url="laptop.jpg"
    )

    ProductService.validate_product(
        category_id=product.category_id or 0,
        name=product.name,
        price=product.price,
        stock=product.stock
    )


def test_create_product_invalid_category():
    """Test product creation with invalid category."""

    product = Product(
        category_id=None,
        name="Laptop",
        description="Test laptop",
        price=50000,
        stock=10,
        image_url="laptop.jpg"
    )

    with pytest.raises(ValueError):
        ProductService.create_product(product)


# ============================================================
# Get Product Tests
# ============================================================

def test_get_product_invalid_id():
    """Test getting a product with invalid ID."""

    with pytest.raises(ValueError):
        ProductService.get_product(0)


def test_get_product_negative_id():
    """Test getting a product with negative ID."""

    with pytest.raises(ValueError):
        ProductService.get_product(-1)


# ============================================================
# Update Product Tests
# ============================================================

def test_update_product_without_id():
    """Test updating a product without product ID."""

    product = Product(
        product_id=None,
        category_id=1,
        name="Laptop",
        description="Test laptop",
        price=50000,
        stock=10,
        image_url="laptop.jpg"
    )

    with pytest.raises(ValueError):
        ProductService.update_product(product)


# ============================================================
# Delete Product Tests
# ============================================================

def test_delete_product_invalid_id():
    """Test deleting a product with invalid ID."""

    with pytest.raises(ValueError):
        ProductService.delete_product(0)


def test_delete_product_negative_id():
    """Test deleting a product with negative ID."""

    with pytest.raises(ValueError):
        ProductService.delete_product(-1)