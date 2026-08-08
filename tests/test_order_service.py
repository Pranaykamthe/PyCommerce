"""
test_order_service.py
---------------------
Tests for OrderService.
"""

import pytest

from models.order import Order
from models.order_item import OrderItem
from services.order_service import OrderService


# ============================================================
# Validation Tests
# ============================================================

def test_valid_user_id():
    """Test valid user ID."""

    OrderService.validate_user_id(1)


def test_invalid_user_id():
    """Test invalid user ID."""

    with pytest.raises(ValueError):
        OrderService.validate_user_id(0)


def test_negative_user_id():
    """Test negative user ID."""

    with pytest.raises(ValueError):
        OrderService.validate_user_id(-1)


def test_valid_status():
    """Test valid order status."""

    OrderService.validate_status(
        "pending"
    )

    OrderService.validate_status(
        "confirmed"
    )

    OrderService.validate_status(
        "shipped"
    )

    OrderService.validate_status(
        "delivered"
    )

    OrderService.validate_status(
        "cancelled"
    )


def test_invalid_status():
    """Test invalid order status."""

    with pytest.raises(ValueError):
        OrderService.validate_status(
            "invalid"
        )


def test_valid_shipping_address():
    """Test valid shipping address."""

    OrderService.validate_shipping_address(
        "Pune, Maharashtra"
    )


def test_empty_shipping_address():
    """Test empty shipping address."""

    with pytest.raises(ValueError):
        OrderService.validate_shipping_address(
            ""
        )


def test_valid_quantity():
    """Test valid quantity."""

    OrderService.validate_quantity(5)


def test_invalid_quantity():
    """Test invalid quantity."""

    with pytest.raises(ValueError):
        OrderService.validate_quantity(0)


def test_negative_quantity():
    """Test negative quantity."""

    with pytest.raises(ValueError):
        OrderService.validate_quantity(-1)


def test_valid_price():
    """Test valid price."""

    OrderService.validate_price(500.00)


def test_negative_price():
    """Test negative price."""

    with pytest.raises(ValueError):
        OrderService.validate_price(-100.00)


# ============================================================
# Total Calculation Tests
# ============================================================

def test_calculate_total():
    """Test calculating order total."""

    items = [
        OrderItem(
            product_id=1,
            quantity=2,
            price=500.00
        ),
        OrderItem(
            product_id=2,
            quantity=1,
            price=250.00
        )
    ]

    total = OrderService.calculate_total(
        items
    )

    assert total == 1250.00


def test_calculate_total_empty_items():
    """Test calculating total without items."""

    with pytest.raises(ValueError):
        OrderService.calculate_total([])


def test_calculate_total_invalid_quantity():
    """Test total calculation with invalid quantity."""

    items = [
        OrderItem(
            product_id=1,
            quantity=0,
            price=500.00
        )
    ]

    with pytest.raises(ValueError):
        OrderService.calculate_total(items)


def test_calculate_total_negative_price():
    """Test total calculation with negative price."""

    items = [
        OrderItem(
            product_id=1,
            quantity=1,
            price=-500.00
        )
    ]

    with pytest.raises(ValueError):
        OrderService.calculate_total(items)


# ============================================================
# Order Validation Tests
# ============================================================

def test_create_order_without_user():
    """Test order without user ID."""

    order = Order(
        user_id=None,
        shipping_address="Pune"
    )

    items = [
        OrderItem(
            product_id=1,
            quantity=1,
            price=100.00
        )
    ]

    with pytest.raises(ValueError):
        OrderService.create_order(
            order,
            items
        )


def test_create_order_without_items():
    """Test order without items."""

    order = Order(
        user_id=1,
        shipping_address="Pune"
    )

    with pytest.raises(ValueError):
        OrderService.create_order(
            order,
            []
        )


def test_update_order_without_id():
    """Test updating an order without ID."""

    order = Order(
        order_id=None,
        user_id=1,
        total_amount=100.00,
        status="pending",
        shipping_address="Pune"
    )

    with pytest.raises(ValueError):
        OrderService.update_order(order)


# ============================================================
# Order Item Validation Tests
# ============================================================

def test_add_order_item_without_order_id():
    """Test order item without order ID."""

    item = OrderItem(
        order_id=None,
        product_id=1,
        quantity=1,
        price=100.00
    )

    with pytest.raises(ValueError):
        OrderService.add_order_item(item)


def test_add_order_item_without_product_id():
    """Test order item without product ID."""

    item = OrderItem(
        order_id=1,
        product_id=None,
        quantity=1,
        price=100.00
    )

    with pytest.raises(ValueError):
        OrderService.add_order_item(item)


def test_update_order_item_without_id():
    """Test updating order item without ID."""

    item = OrderItem(
        order_item_id=None,
        order_id=1,
        product_id=1,
        quantity=1,
        price=100.00
    )

    with pytest.raises(ValueError):
        OrderService.update_order_item(item)


# ============================================================
# ID Validation Tests
# ============================================================

def test_get_order_invalid_id():
    """Test invalid order ID."""

    with pytest.raises(ValueError):
        OrderService.get_order(0)


def test_get_user_orders_invalid_id():
    """Test invalid user ID."""

    with pytest.raises(ValueError):
        OrderService.get_user_orders(0)


def test_get_order_items_invalid_id():
    """Test invalid order ID."""

    with pytest.raises(ValueError):
        OrderService.get_order_items(0)


def test_delete_order_invalid_id():
    """Test invalid order ID."""

    with pytest.raises(ValueError):
        OrderService.delete_order(0)


def test_delete_order_item_invalid_id():
    """Test invalid order item ID."""

    with pytest.raises(ValueError):
        OrderService.delete_order_item(0)