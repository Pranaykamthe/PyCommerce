from types import SimpleNamespace

from utils.tables import (
    create_table,
    show_product_table,
    show_customer_table,
    show_order_table,
    show_cart_table,
)


def test_create_table():
    """Test generic table creation."""

    table = create_table(
        "Test Table",
        ["ID", "Name"],
    )

    assert table is not None
    assert len(table.columns) == 2


def test_show_product_table():
    """Test product table."""

    products = [
        SimpleNamespace(
            product_id=1,
            name="Laptop",
            price=50000.00,
            stock=10,
        ),
        SimpleNamespace(
            product_id=2,
            name="Mouse",
            price=800.00,
            stock=25,
        ),
    ]

    show_product_table(products)


def test_show_customer_table():
    """Test customer table."""

    customers = [
        SimpleNamespace(
            customer_id=1,
            name="Pranay",
            email="pranay@example.com",
        ),
    ]

    show_customer_table(customers)


def test_show_order_table():
    """Test order table."""

    orders = [
        SimpleNamespace(
            order_id=101,
            customer_id=1,
            total_amount=50800.00,
            status="Completed",
        ),
    ]

    show_order_table(orders)


def test_show_cart_table():
    """Test shopping cart table."""

    cart_items = [
        SimpleNamespace(
            product_id=1,
            product_name="Laptop",
            quantity=1,
            price=50000.00,
        ),
    ]

    show_cart_table(cart_items)