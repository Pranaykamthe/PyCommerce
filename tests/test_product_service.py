import pytest

from models.product import Product
from services.product_service import ProductService


def test_validate_product():
    ProductService.validate_product(
        name="Laptop",
        price=50000,
        stock=10
    )


def test_empty_product_name():
    with pytest.raises(ValueError):
        ProductService.validate_product(
            name="",
            price=50000,
            stock=10
        )


def test_negative_price():
    with pytest.raises(ValueError):
        ProductService.validate_product(
            name="Laptop",
            price=-100,
            stock=10
        )


def test_negative_stock():
    with pytest.raises(ValueError):
        ProductService.validate_product(
            name="Laptop",
            price=50000,
            stock=-1
        )


def test_product_available():
    product = Product(
        name="Laptop",
        description="Test laptop",
        price=50000,
        stock=10
    )

    assert ProductService.is_available(product) is True


def test_product_not_available():
    product = Product(
        name="Laptop",
        description="Test laptop",
        price=50000,
        stock=0
    )

    assert ProductService.is_available(product) is False


def test_increase_stock():
    product = Product(
        name="Laptop",
        description="Test laptop",
        price=50000,
        stock=10
    )

    ProductService.increase_stock(product, 5)

    assert product.stock == 15


def test_decrease_stock():
    product = Product(
        name="Laptop",
        description="Test laptop",
        price=50000,
        stock=10
    )

    ProductService.decrease_stock(product, 3)

    assert product.stock == 7


def test_decrease_stock_insufficient():
    product = Product(
        name="Laptop",
        description="Test laptop",
        price=50000,
        stock=2
    )

    with pytest.raises(ValueError):
        ProductService.decrease_stock(product, 5)