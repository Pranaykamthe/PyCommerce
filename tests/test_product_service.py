"""
Tests for ProductService.
"""

import pytest

from unittest.mock import patch
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
# Get Products By Category Tests
# ============================================================

def test_get_products_by_category_invalid_id():
    """Test retrieving products with an invalid category ID."""

    with pytest.raises(ValueError):
        ProductService.get_products_by_category(0)


def test_get_products_by_category_negative_id():
    """Test retrieving products with a negative category ID."""

    with pytest.raises(ValueError):
        ProductService.get_products_by_category(-1)


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


# ============================================================
# ProductService Business Logic Tests
# ============================================================

def test_create_product():
    """Test creating a product through ProductService."""

    product = Product(
        category_id=1,
        name="  Test Product  ",
        description="  Test Description  ",
        price=999.99,
        stock=10,
        image_url="  test.jpg  "
    )

    with patch(
        "services.product_service.ProductRepository.create",
        return_value=product
    ) as mock_create:

        result = ProductService.create_product(product)

    assert result is product

    assert product.name == "Test Product"
    assert product.description == "Test Description"
    assert product.image_url == "test.jpg"

    mock_create.assert_called_once_with(
        product
    )


def test_create_product_without_category():
    """Test creating a product without a category."""

    product = Product(
        category_id=None,
        name="Test Product",
        description="Test Description",
        price=100.00,
        stock=5,
        image_url="test.jpg"
    )

    with pytest.raises(ValueError):
        ProductService.create_product(product)


def test_get_product():
    """Test retrieving a product by ID."""

    product = Product(
        product_id=1,
        category_id=1,
        name="Test Product",
        description="Test Description",
        price=500.00,
        stock=10,
        image_url="test.jpg"
    )

    with patch(
        "services.product_service.ProductRepository.get_by_id",
        return_value=product
    ) as mock_get:

        result = ProductService.get_product(1)

    assert result is product

    mock_get.assert_called_once_with(1)


def test_get_product_not_found():
    """Test retrieving a product that does not exist."""

    with patch(
        "services.product_service.ProductRepository.get_by_id",
        return_value=None
    ) as mock_get:

        result = ProductService.get_product(999999)

    assert result is None

    mock_get.assert_called_once_with(999999)


def test_get_all_products():
    """Test retrieving all products."""

    products = [
        Product(
            product_id=1,
            category_id=1,
            name="Product One",
            description="Description One",
            price=100.00,
            stock=10,
            image_url="one.jpg"
        ),
        Product(
            product_id=2,
            category_id=1,
            name="Product Two",
            description="Description Two",
            price=200.00,
            stock=20,
            image_url="two.jpg"
        )
    ]

    with patch(
        "services.product_service.ProductRepository.get_all",
        return_value=products
    ) as mock_get:

        result = ProductService.get_all_products()

    assert result == products
    assert len(result) == 2

    mock_get.assert_called_once_with()


def test_get_products_by_category():
    """Test retrieving products by category."""

    products = [
        Product(
            product_id=1,
            category_id=2,
            name="Category Product",
            description="Test Product",
            price=300.00,
            stock=15,
            image_url="category.jpg"
        )
    ]

    with patch(
        "services.product_service.ProductRepository.get_by_category",
        return_value=products
    ) as mock_get:

        result = ProductService.get_products_by_category(2)

    assert result == products
    assert result[0].category_id == 2

    mock_get.assert_called_once_with(2)


def test_get_products_by_category_empty():
    """Test category search when no products are found."""

    with patch(
        "services.product_service.ProductRepository.get_by_category",
        return_value=[]
    ) as mock_get:

        result = ProductService.get_products_by_category(1)

    assert result == []

    mock_get.assert_called_once_with(1)


def test_search_products():
    """Test searching products by name."""

    products = [
        Product(
            product_id=1,
            category_id=1,
            name="Laptop",
            description="Test Laptop",
            price=50000.00,
            stock=5,
            image_url="laptop.jpg"
        )
    ]

    with patch(
        "services.product_service.ProductRepository.search_by_name",
        return_value=products
    ) as mock_search:

        result = ProductService.search_products(
            "  Laptop  "
        )

    assert result == products
    assert result[0].name == "Laptop"

    mock_search.assert_called_once_with(
        "Laptop"
    )


def test_search_products_not_found():
    """Test searching when no products match."""

    with patch(
        "services.product_service.ProductRepository.search_by_name",
        return_value=[]
    ) as mock_search:

        result = ProductService.search_products(
            "Nonexistent"
        )

    assert result == []

    mock_search.assert_called_once_with(
        "Nonexistent"
    )


def test_search_products_empty_term():
    """Test searching products with an empty search term."""

    with pytest.raises(ValueError):
        ProductService.search_products("")


def test_search_products_whitespace_term():
    """Test searching products with a whitespace-only search term."""

    with pytest.raises(ValueError):
        ProductService.search_products("   ")


def test_update_product():
    """Test updating an existing product."""

    product = Product(
        product_id=1,
        category_id=1,
        name="  Updated Product  ",
        description="  Updated Description  ",
        price=1500.00,
        stock=25,
        image_url="  updated.jpg  "
    )

    with patch(
        "services.product_service.ProductRepository.update",
        return_value=True
    ) as mock_update:

        result = ProductService.update_product(product)

    assert result is True

    assert product.name == "Updated Product"
    assert product.description == "Updated Description"
    assert product.image_url == "updated.jpg"

    mock_update.assert_called_once_with(
        product
    )


def test_update_product_failed():
    """Test when product update fails."""

    product = Product(
        product_id=1,
        category_id=1,
        name="Updated Product",
        description="Description",
        price=1500.00,
        stock=25,
        image_url="updated.jpg"
    )

    with patch(
        "services.product_service.ProductRepository.update",
        return_value=False
    ) as mock_update:

        result = ProductService.update_product(product)

    assert result is False

    mock_update.assert_called_once_with(
        product
    )


def test_delete_product():
    """Test deleting a product."""

    with patch(
        "services.product_service.ProductRepository.delete",
        return_value=True
    ) as mock_delete:

        result = ProductService.delete_product(1)

    assert result is True

    mock_delete.assert_called_once_with(1)


def test_delete_product_not_found():
    """Test deleting a product that does not exist."""

    with patch(
        "services.product_service.ProductRepository.delete",
        return_value=False
    ) as mock_delete:

        result = ProductService.delete_product(999999)

    assert result is False

    mock_delete.assert_called_once_with(999999)


def test_create_product_repository_failure():
    """Test product creation when repository returns None."""

    product = Product(
        category_id=1,
        name="Test Product",
        description="Description",
        price=100.00,
        stock=5,
        image_url="test.jpg"
    )

    with patch(
        "services.product_service.ProductRepository.create",
        return_value=None
    ) as mock_create:

        result = ProductService.create_product(product)

    assert result is None

    mock_create.assert_called_once_with(
        product
    )


def test_search_products_empty_result():
    """Test product search when no products are found."""

    with patch(
        "services.product_service.ProductRepository.search_by_name",
        return_value=[]
    ) as mock_search:

        result = ProductService.search_products(
            "Unknown Product"
        )

    assert result == []

    mock_search.assert_called_once_with(
        "Unknown Product"
    )