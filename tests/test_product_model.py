"""
test_product_model.py
---------------------
Tests for the Product model.
"""

from models.product import Product


def test_create_product():
    """Test creating a product."""

    product = Product(
        product_id=101,
        category_id=1,
        name="Wireless Mouse",
        description="2.4 GHz wireless mouse",
        price=799.00,
        stock=25,
        image_url="images/mouse.jpg",
    )

    assert product.product_id == 101
    assert product.category_id == 1
    assert product.name == "Wireless Mouse"
    assert product.description == "2.4 GHz wireless mouse"
    assert product.price == 799.00
    assert product.stock == 25
    assert product.image_url == "images/mouse.jpg"


def test_product_default_values():
    """Test product default values."""

    product = Product()

    assert product.product_id is None
    assert product.category_id is None
    assert product.name == ""
    assert product.description == ""
    assert product.price == 0.0
    assert product.stock == 0
    assert product.image_url == ""
    assert product.created_at is None
    assert product.updated_at is None


def test_product_string():
    """Test Product string representation."""

    product = Product(
        product_id=101,
        name="Laptop",
        price=55000.00,
        stock=10,
    )

    result = str(product)

    assert "Laptop" in result
    assert "55000.0" in result
    assert "10" in result