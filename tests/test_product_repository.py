"""
test_product_repository.py
--------------------------
Integration tests for ProductRepository.

These tests interact with the MySQL database.
"""

from models.product import Product
from repositories.product_repository import ProductRepository


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

    # Store ID for the remaining CRUD operations.
    product_id = created_product.product_id

    # Verify that the created product can be retrieved.
    saved_product = ProductRepository.get_by_id(product_id)

    assert saved_product is not None
    assert saved_product.product_id == product_id
    assert saved_product.name == "Test Product PyCommerce"
    assert saved_product.price == 999.99
    assert saved_product.stock == 10

    # Clean up the test product.
    ProductRepository.delete(product_id)


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


def test_get_all_products():
    """Test retrieving all products."""

    products = ProductRepository.get_all()

    assert isinstance(products, list)


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

    result = ProductRepository.update(product)

    assert result is False


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