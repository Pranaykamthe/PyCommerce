"""
test_order_item_model.py
------------------------
Tests for the OrderItem model.
"""

from models.order_item import OrderItem


def test_create_order_item():
    """Test creating an order item."""

    item = OrderItem(
        order_item_id=1,
        order_id=5001,
        product_id=101,
        quantity=2,
        price=799.00,
    )

    assert item.order_item_id == 1
    assert item.order_id == 5001
    assert item.product_id == 101
    assert item.quantity == 2
    assert item.price == 799.00


def test_order_item_default_values():
    """Test order item default values."""

    item = OrderItem()

    assert item.order_item_id is None
    assert item.order_id is None
    assert item.product_id is None
    assert item.quantity == 1
    assert item.price == 0.0


def test_order_item_string():
    """Test OrderItem string representation."""

    item = OrderItem(
        order_item_id=1,
        order_id=5001,
        product_id=101,
        quantity=2,
        price=799.00,
    )

    result = str(item)

    assert "1" in result
    assert "5001" in result
    assert "101" in result
    assert "2" in result
    assert "799.0" in result