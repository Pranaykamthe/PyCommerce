"""
Integration tests for ProductRepository.

These tests interact with the MySQL database.
"""
from unittest.mock import patch
from models.product import Product
from repositories.product_repository import ProductRepository


# ============================================================
# Create Product
# ============================================================

def test_create_product():
    """Test creating a product in MySQL."""

    product = Product(
        category_id=1,
        name="Test Product PyCommerce",
        description="Temporary test product",
        price=999.99,
        stock=10,
        image_url="test.jpg"
    )

    created_product = ProductRepository.create(product)

    assert created_product is not None
    assert created_product.product_id is not None

    product_id = created_product.product_id

    saved_product = ProductRepository.get_by_id(
        product_id
    )

    assert saved_product is not None
    assert saved_product.product_id == product_id
    assert saved_product.name == "Test Product PyCommerce"
    assert saved_product.price == 999.99
    assert saved_product.stock == 10

    ProductRepository.delete(product_id)


# ============================================================
# Get Product By ID
# ============================================================

def test_get_product_by_id():
    """Test retrieving a product by ID."""

    product = Product(
        category_id=1,
        name="Read Test Product",
        description="Product read test",
        price=500.00,
        stock=5,
        image_url="read-test.jpg"
    )

    created_product = ProductRepository.create(product)

    assert created_product is not None
    assert created_product.product_id is not None

    product_id = created_product.product_id

    retrieved_product = ProductRepository.get_by_id(
        product_id
    )

    assert retrieved_product is not None
    assert retrieved_product.product_id == product_id
    assert retrieved_product.name == "Read Test Product"

    ProductRepository.delete(product_id)


def test_get_product_not_found():
    """Test retrieving a product that does not exist."""

    product = ProductRepository.get_by_id(
        999999999
    )

    assert product is None


# ============================================================
# Get All Products
# ============================================================

def test_get_all_products():
    """Test retrieving all products."""

    products = ProductRepository.get_all()

    assert isinstance(products, list)


# ============================================================
# Get Products By Category
# ============================================================

def test_get_products_by_category():
    """Test retrieving products belonging to a category."""

    product = Product(
        category_id=1,
        name="Category Test Product",
        description="Category test",
        price=750.00,
        stock=10,
        image_url="category-test.jpg"
    )

    created_product = ProductRepository.create(product)

    assert created_product is not None
    assert created_product.product_id is not None

    product_id = created_product.product_id

    try:
        products = ProductRepository.get_by_category(
            1
        )

        assert isinstance(products, list)

        matching_products = [
            item
            for item in products
            if item.product_id == product_id
        ]

        assert len(matching_products) == 1
        assert matching_products[0].name == (
            "Category Test Product"
        )

    finally:
        ProductRepository.delete(product_id)


def test_get_products_by_invalid_category():
    """Test retrieving products with invalid category ID."""

    result = ProductRepository.get_by_category(
        0
    )

    assert result == []


def test_get_products_by_negative_category():
    """Test retrieving products with negative category ID."""

    result = ProductRepository.get_by_category(
        -1
    )

    assert result == []


# ============================================================
# Search Products By Name
# ============================================================

def test_search_products_by_name():
    """Test searching products by partial name."""

    product = Product(
        category_id=1,
        name="Unique Search Product PyCommerce",
        description="Search test",
        price=650.00,
        stock=8,
        image_url="search-test.jpg"
    )

    created_product = ProductRepository.create(product)

    assert created_product is not None
    assert created_product.product_id is not None

    product_id = created_product.product_id

    try:
        products = ProductRepository.search_by_name(
            "Unique Search Product"
        )

        assert isinstance(products, list)

        matching_products = [
            item
            for item in products
            if item.product_id == product_id
        ]

        assert len(matching_products) == 1
        assert matching_products[0].name == (
            "Unique Search Product PyCommerce"
        )

    finally:
        ProductRepository.delete(product_id)


def test_search_product_not_found():
    """Test searching for a product that does not exist."""

    products = ProductRepository.search_by_name(
        "ProductThatDefinitelyDoesNotExist999999"
    )

    assert isinstance(products, list)
    assert products == []


# ============================================================
# Update Product
# ============================================================

def test_update_product():
    """Test updating a product."""

    product = Product(
        category_id=1,
        name="Update Test Product",
        description="Original description",
        price=1000.00,
        stock=20,
        image_url="original.jpg"
    )

    created_product = ProductRepository.create(product)

    assert created_product is not None
    assert created_product.product_id is not None

    created_product.name = "Updated Test Product"
    created_product.description = "Updated description"
    created_product.price = 1500.00
    created_product.stock = 25
    created_product.image_url = "updated.jpg"

    result = ProductRepository.update(
        created_product
    )

    assert result is True

    updated_product = ProductRepository.get_by_id(
        created_product.product_id
    )

    assert updated_product is not None
    assert updated_product.name == "Updated Test Product"
    assert updated_product.description == "Updated description"
    assert updated_product.price == 1500.00
    assert updated_product.stock == 25
    assert updated_product.image_url == "updated.jpg"

    ProductRepository.delete(
        created_product.product_id
    )


def test_update_product_without_id():
    """Test updating a product without an ID."""

    product = Product(
        product_id=None,
        category_id=1,
        name="Invalid Update",
        description="Test",
        price=100.00,
        stock=5,
        image_url=""
    )

    result = ProductRepository.update(
        product
    )

    assert result is False


# ============================================================
# Decrease Stock
# ============================================================

def test_decrease_stock():
    """Test decreasing product stock."""

    product = Product(
        category_id=1,
        name="Stock Test Product",
        description="Stock decrease test",
        price=300.00,
        stock=10,
        image_url="stock-test.jpg"
    )

    created_product = ProductRepository.create(product)

    assert created_product is not None
    assert created_product.product_id is not None

    product_id = created_product.product_id

    try:
        result = ProductRepository.decrease_stock(
            product_id,
            3
        )

        assert result is True

        updated_product = (
            ProductRepository.get_by_id(
                product_id
            )
        )

        assert updated_product is not None
        assert updated_product.stock == 7

    finally:
        ProductRepository.delete(product_id)


def test_decrease_stock_insufficient_stock():
    """Test decreasing stock when there is not enough stock."""

    product = Product(
        category_id=1,
        name="Insufficient Stock Product",
        description="Insufficient stock test",
        price=400.00,
        stock=5,
        image_url="insufficient-stock.jpg"
    )

    created_product = ProductRepository.create(product)

    assert created_product is not None
    assert created_product.product_id is not None

    product_id = created_product.product_id

    try:
        result = ProductRepository.decrease_stock(
            product_id,
            10
        )

        assert result is False

        unchanged_product = (
            ProductRepository.get_by_id(
                product_id
            )
        )

        assert unchanged_product is not None
        assert unchanged_product.stock == 5

    finally:
        ProductRepository.delete(product_id)


def test_decrease_stock_invalid_product_id():
    """Test decreasing stock with an invalid product ID."""

    result = ProductRepository.decrease_stock(
        0,
        2
    )

    assert result is False


def test_decrease_stock_negative_product_id():
    """Test decreasing stock with a negative product ID."""

    result = ProductRepository.decrease_stock(
        -1,
        2
    )

    assert result is False


def test_decrease_stock_invalid_quantity():
    """Test decreasing stock with zero quantity."""

    result = ProductRepository.decrease_stock(
        1,
        0
    )

    assert result is False


def test_decrease_stock_negative_quantity():
    """Test decreasing stock with negative quantity."""

    result = ProductRepository.decrease_stock(
        1,
        -2
    )

    assert result is False


# ============================================================
# Delete Product
# ============================================================

def test_delete_product():
    """Test deleting a product."""

    product = Product(
        category_id=1,
        name="Delete Test Product",
        description="Product deletion test",
        price=250.00,
        stock=5,
        image_url="delete-test.jpg"
    )

    created_product = ProductRepository.create(product)

    assert created_product is not None
    assert created_product.product_id is not None

    product_id = created_product.product_id

    result = ProductRepository.delete(
        product_id
    )

    assert result is True

    deleted_product = ProductRepository.get_by_id(
        product_id
    )

    assert deleted_product is None


def test_delete_product_not_found():
    """Test deleting a product that does not exist."""

    result = ProductRepository.delete(
        999999999
    )

    assert result is False


def test_delete_product_invalid_id():
    """Test deleting a product with an invalid ID."""

    result = ProductRepository.delete(
        0
    )

    assert result is False


def test_delete_product_negative_id():
    """Test deleting a product with a negative ID."""

    result = ProductRepository.delete(
        -1
    )

    assert result is False

# ============================================================
# Database Connection Failure Tests
# ============================================================

def test_create_product_without_connection():
    """Test create when database connection is unavailable."""

    product = Product(
        category_id=1,
        name="Connection Test Product",
        description="Test",
        price=100.00,
        stock=5,
        image_url=""
    )

    with patch(
        "repositories.product_repository.get_connection",
        return_value=None
    ):
        result = ProductRepository.create(product)

    assert result is None


def test_get_product_by_id_without_connection():
    """Test get_by_id when database connection is unavailable."""

    with patch(
        "repositories.product_repository.get_connection",
        return_value=None
    ):
        result = ProductRepository.get_by_id(1)

    assert result is None


def test_get_all_products_without_connection():
    """Test get_all when database connection is unavailable."""

    with patch(
        "repositories.product_repository.get_connection",
        return_value=None
    ):
        result = ProductRepository.get_all()

    assert result == []


def test_get_products_by_category_without_connection():
    """Test category lookup when database connection is unavailable."""

    with patch(
        "repositories.product_repository.get_connection",
        return_value=None
    ):
        result = ProductRepository.get_by_category(1)

    assert result == []


def test_search_products_without_connection():
    """Test product search when database connection is unavailable."""

    with patch(
        "repositories.product_repository.get_connection",
        return_value=None
    ):
        result = ProductRepository.search_by_name(
            "Test"
        )

    assert result == []


def test_update_product_without_connection():
    """Test update when database connection is unavailable."""

    product = Product(
        product_id=1,
        category_id=1,
        name="Connection Test Product",
        description="Test",
        price=100.00,
        stock=5,
        image_url=""
    )

    with patch(
        "repositories.product_repository.get_connection",
        return_value=None
    ):
        result = ProductRepository.update(product)

    assert result is False


def test_decrease_stock_without_connection():
    """Test stock decrease when database connection is unavailable."""

    with patch(
        "repositories.product_repository.get_connection",
        return_value=None
    ):
        result = ProductRepository.decrease_stock(
            1,
            2
        )

    assert result is False


def test_delete_product_without_connection():
    """Test delete when database connection is unavailable."""

    with patch(
        "repositories.product_repository.get_connection",
        return_value=None
    ):
        result = ProductRepository.delete(1)

    assert result is False