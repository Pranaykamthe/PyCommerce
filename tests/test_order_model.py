"""
test_order_model.py
-------------------
Tests for the Order model.
"""

from models.order import Order


def test_create_order():
    """Test creating an order."""

    order = Order(
        order_id=5001,
        user_id=10,
        total_amount=1598.00,
        status="pending",
        shipping_address="Pune, Maharashtra",
    )

    assert order.order_id == 5001
    assert order.user_id == 10
    assert order.total_amount == 1598.00
    assert order.status == "pending"
    assert order.shipping_address == "Pune, Maharashtra"


def test_order_default_values():
    """Test order default values."""

    order = Order()

    assert order.order_id is None
    assert order.user_id is None
    assert order.total_amount == 0.0
    assert order.status == "pending"
    assert order.shipping_address == ""
    assert order.created_at is None
    assert order.updated_at is None


def test_order_string():
    """Test Order string representation."""

    order = Order(
        order_id=5001,
        user_id=10,
        total_amount=1598.00,
        status="confirmed",
    )

    result = str(order)

    assert "5001" in result
    assert "10" in result
    assert "1598.0" in result
    assert "confirmed" in result