"""
test_order_service.py
---------------------
Tests for OrderService business logic.
"""

import pytest

from models.order import Order
from models.order_item import OrderItem
from repositories.order_repository import OrderRepository
from services.order_service import OrderService


# ============================================================
# Validation - User ID
# ============================================================

def test_validate_user_id():
    """Test valid user ID."""

    OrderService.validate_user_id(1)


def test_validate_user_id_none():
    """Test None user ID."""

    with pytest.raises(ValueError):
        OrderService.validate_user_id(None)


def test_validate_user_id_zero():
    """Test zero user ID."""

    with pytest.raises(ValueError):
        OrderService.validate_user_id(0)


def test_validate_user_id_negative():
    """Test negative user ID."""

    with pytest.raises(ValueError):
        OrderService.validate_user_id(-1)


# ============================================================
# Validation - Status
# ============================================================

def test_validate_status():
    """Test valid order statuses."""

    OrderService.validate_status("pending")
    OrderService.validate_status("confirmed")
    OrderService.validate_status("shipped")
    OrderService.validate_status("delivered")
    OrderService.validate_status("cancelled")


def test_validate_status_invalid():
    """Test invalid order status."""

    with pytest.raises(ValueError):
        OrderService.validate_status("invalid")


# ============================================================
# Validation - Shipping Address
# ============================================================

def test_validate_shipping_address():
    """Test valid shipping address."""

    OrderService.validate_shipping_address("Pune")


def test_validate_shipping_address_empty():
    """Test empty shipping address."""

    with pytest.raises(ValueError):
        OrderService.validate_shipping_address("")


def test_validate_shipping_address_whitespace():
    """Test whitespace-only shipping address."""

    with pytest.raises(ValueError):
        OrderService.validate_shipping_address("   ")


# ============================================================
# Validation - Quantity
# ============================================================

def test_validate_quantity():
    """Test valid quantity."""

    OrderService.validate_quantity(1)
    OrderService.validate_quantity(10)


def test_validate_quantity_zero():
    """Test zero quantity."""

    with pytest.raises(ValueError):
        OrderService.validate_quantity(0)


def test_validate_quantity_negative():
    """Test negative quantity."""

    with pytest.raises(ValueError):
        OrderService.validate_quantity(-1)


# ============================================================
# Validation - Price
# ============================================================

def test_validate_price():
    """Test valid price."""

    OrderService.validate_price(0)
    OrderService.validate_price(100.50)


def test_validate_price_negative():
    """Test negative price."""

    with pytest.raises(ValueError):
        OrderService.validate_price(-1)


# ============================================================
# Calculate Total
# ============================================================

def test_calculate_total():
    """Test calculating order total."""

    items = [
        OrderItem(
            product_id=1,
            quantity=2,
            price=100.00
        ),
        OrderItem(
            product_id=2,
            quantity=3,
            price=50.00
        )
    ]

    total = OrderService.calculate_total(items)

    assert total == 350.00


def test_calculate_total_single_item():
    """Test calculating total for one item."""

    items = [
        OrderItem(
            product_id=1,
            quantity=2,
            price=250.00
        )
    ]

    total = OrderService.calculate_total(items)

    assert total == 500.00


def test_calculate_total_rounding():
    """Test total rounding."""

    items = [
        OrderItem(
            product_id=1,
            quantity=3,
            price=10.333
        )
    ]

    total = OrderService.calculate_total(items)

    assert total == 31.00


def test_calculate_total_empty():
    """Test calculating total with no items."""

    with pytest.raises(ValueError):
        OrderService.calculate_total([])


def test_calculate_total_invalid_quantity():
    """Test total calculation with zero quantity."""

    items = [
        OrderItem(
            product_id=1,
            quantity=0,
            price=100.00
        )
    ]

    with pytest.raises(ValueError):
        OrderService.calculate_total(items)


def test_calculate_total_negative_quantity():
    """Test total calculation with negative quantity."""

    items = [
        OrderItem(
            product_id=1,
            quantity=-1,
            price=100.00
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
            price=-100.00
        )
    ]

    with pytest.raises(ValueError):
        OrderService.calculate_total(items)


# ============================================================
# Create Order
# ============================================================

def test_create_order(monkeypatch):
    """Test creating an order."""

    order = Order(
        user_id=1,
        total_amount=0,
        status="pending",
        shipping_address=" Pune "
    )

    items = [
        OrderItem(
            product_id=1,
            quantity=2,
            price=250.00
        )
    ]

    created_order = Order(
        order_id=100,
        user_id=1,
        total_amount=500.00,
        status="pending",
        shipping_address="Pune"
    )

    monkeypatch.setattr(
        OrderRepository,
        "create_order",
        lambda order: created_order
    )

    monkeypatch.setattr(
        OrderRepository,
        "create_order_item",
        lambda item: item
    )

    result = OrderService.create_order(
        order,
        items
    )

    assert result == created_order
    assert order.total_amount == 500.00
    assert order.shipping_address == "Pune"
    assert items[0].order_id == 100


def test_create_order_multiple_items(monkeypatch):
    """Test creating an order with multiple items."""

    order = Order(
        user_id=1,
        total_amount=0,
        status="pending",
        shipping_address="Pune"
    )

    items = [
        OrderItem(
            product_id=1,
            quantity=2,
            price=100.00
        ),
        OrderItem(
            product_id=2,
            quantity=3,
            price=50.00
        )
    ]

    created_order = Order(
        order_id=101,
        user_id=1,
        total_amount=350.00,
        status="pending",
        shipping_address="Pune"
    )

    monkeypatch.setattr(
        OrderRepository,
        "create_order",
        lambda order: created_order
    )

    monkeypatch.setattr(
        OrderRepository,
        "create_order_item",
        lambda item: item
    )

    result = OrderService.create_order(
        order,
        items
    )

    assert result == created_order
    assert order.total_amount == 350.00
    assert items[0].order_id == 101
    assert items[1].order_id == 101


def test_create_order_invalid_user():
    """Test creating order with invalid user."""

    order = Order(
        user_id=0,
        total_amount=100,
        status="pending",
        shipping_address="Pune"
    )

    items = [
        OrderItem(
            product_id=1,
            quantity=1,
            price=100
        )
    ]

    with pytest.raises(ValueError):
        OrderService.create_order(
            order,
            items
        )


def test_create_order_invalid_status():
    """Test creating order with invalid status."""

    order = Order(
        user_id=1,
        total_amount=100,
        status="invalid",
        shipping_address="Pune"
    )

    items = [
        OrderItem(
            product_id=1,
            quantity=1,
            price=100
        )
    ]

    with pytest.raises(ValueError):
        OrderService.create_order(
            order,
            items
        )


def test_create_order_invalid_address():
    """Test creating order with invalid address."""

    order = Order(
        user_id=1,
        total_amount=100,
        status="pending",
        shipping_address="   "
    )

    items = [
        OrderItem(
            product_id=1,
            quantity=1,
            price=100
        )
    ]

    with pytest.raises(ValueError):
        OrderService.create_order(
            order,
            items
        )


def test_create_order_empty_items():
    """Test creating order without items."""

    order = Order(
        user_id=1,
        total_amount=0,
        status="pending",
        shipping_address="Pune"
    )

    with pytest.raises(ValueError):
        OrderService.create_order(
            order,
            []
        )


def test_create_order_repository_returns_none(monkeypatch):
    """Test when order repository returns None."""

    order = Order(
        user_id=1,
        total_amount=0,
        status="pending",
        shipping_address="Pune"
    )

    items = [
        OrderItem(
            product_id=1,
            quantity=1,
            price=100
        )
    ]

    monkeypatch.setattr(
        OrderRepository,
        "create_order",
        lambda order: None
    )

    result = OrderService.create_order(
        order,
        items
    )

    assert result is None


def test_create_order_item_failure(monkeypatch):
    """Test cleanup when order item creation fails."""

    order = Order(
        user_id=1,
        total_amount=0,
        status="pending",
        shipping_address="Pune"
    )

    items = [
        OrderItem(
            product_id=1,
            quantity=1,
            price=100
        )
    ]

    created_order = Order(
        order_id=200,
        user_id=1,
        total_amount=100,
        status="pending",
        shipping_address="Pune"
    )

    deleted = []

    monkeypatch.setattr(
        OrderRepository,
        "create_order",
        lambda order: created_order
    )

    monkeypatch.setattr(
        OrderRepository,
        "create_order_item",
        lambda item: None
    )

    monkeypatch.setattr(
        OrderRepository,
        "delete_order",
        lambda order_id: deleted.append(order_id) or True
    )

    with pytest.raises(RuntimeError):
        OrderService.create_order(
            order,
            items
        )

    assert deleted == [200]


def test_create_order_item_exception(monkeypatch):
    """Test cleanup when order item creation raises an exception."""

    order = Order(
        user_id=1,
        total_amount=0,
        status="pending",
        shipping_address="Pune"
    )

    items = [
        OrderItem(
            product_id=1,
            quantity=1,
            price=100
        )
    ]

    created_order = Order(
        order_id=201,
        user_id=1,
        total_amount=100,
        status="pending",
        shipping_address="Pune"
    )

    deleted = []

    monkeypatch.setattr(
        OrderRepository,
        "create_order",
        lambda order: created_order
    )

    def raise_exception(item):
        raise RuntimeError("Database error")

    monkeypatch.setattr(
        OrderRepository,
        "create_order_item",
        raise_exception
    )

    monkeypatch.setattr(
        OrderRepository,
        "delete_order",
        lambda order_id: deleted.append(order_id) or True
    )

    with pytest.raises(RuntimeError):
        OrderService.create_order(
            order,
            items
        )

    assert deleted == [201]


# ============================================================
# Get Order
# ============================================================

def test_get_order_invalid_id():
    """Test invalid order ID."""

    with pytest.raises(ValueError):
        OrderService.get_order(0)


def test_get_order_negative_id():
    """Test negative order ID."""

    with pytest.raises(ValueError):
        OrderService.get_order(-1)


def test_get_order(monkeypatch):
    """Test retrieving an order."""

    expected_order = Order(
        order_id=1,
        user_id=1,
        total_amount=500.00,
        status="pending",
        shipping_address="Pune"
    )

    monkeypatch.setattr(
        OrderRepository,
        "get_order_by_id",
        lambda order_id: expected_order
    )

    result = OrderService.get_order(1)

    assert result == expected_order


def test_get_order_not_found(monkeypatch):
    """Test order not found."""

    monkeypatch.setattr(
        OrderRepository,
        "get_order_by_id",
        lambda order_id: None
    )

    result = OrderService.get_order(999)

    assert result is None


# ============================================================
# Get All Orders
# ============================================================

def test_get_all_orders(monkeypatch):
    """Test retrieving all orders."""

    expected_orders = [
        Order(
            order_id=1,
            user_id=1,
            total_amount=500.00,
            status="pending",
            shipping_address="Pune"
        ),
        Order(
            order_id=2,
            user_id=2,
            total_amount=750.00,
            status="confirmed",
            shipping_address="Mumbai"
        )
    ]

    monkeypatch.setattr(
        OrderRepository,
        "get_all_orders",
        lambda: expected_orders
    )

    result = OrderService.get_all_orders()

    assert result == expected_orders
    assert len(result) == 2


# ============================================================
# Get User Orders
# ============================================================

def test_get_user_orders_invalid():
    """Test invalid user ID."""

    with pytest.raises(ValueError):
        OrderService.get_user_orders(0)


def test_get_user_orders_negative():
    """Test negative user ID."""

    with pytest.raises(ValueError):
        OrderService.get_user_orders(-1)


def test_get_user_orders(monkeypatch):
    """Test retrieving user orders."""

    expected_orders = [
        Order(
            order_id=1,
            user_id=1,
            total_amount=500.00,
            status="pending",
            shipping_address="Pune"
        )
    ]

    monkeypatch.setattr(
        OrderRepository,
        "get_orders_by_user",
        lambda user_id: expected_orders
    )

    result = OrderService.get_user_orders(1)

    assert result == expected_orders


def test_get_user_orders_empty(monkeypatch):
    """Test user with no orders."""

    monkeypatch.setattr(
        OrderRepository,
        "get_orders_by_user",
        lambda user_id: []
    )

    result = OrderService.get_user_orders(1)

    assert result == []


# ============================================================
# Get Order Items
# ============================================================

def test_get_order_items_invalid():
    """Test invalid order ID."""

    with pytest.raises(ValueError):
        OrderService.get_order_items(0)


def test_get_order_items(monkeypatch):
    """Test retrieving order items."""

    expected_items = [
        OrderItem(
            order_item_id=1,
            order_id=10,
            product_id=1,
            quantity=2,
            price=100.00
        )
    ]

    monkeypatch.setattr(
        OrderRepository,
        "get_order_items",
        lambda order_id: expected_items
    )

    result = OrderService.get_order_items(10)

    assert result == expected_items


def test_get_order_items_empty(monkeypatch):
    """Test order with no items."""

    monkeypatch.setattr(
        OrderRepository,
        "get_order_items",
        lambda order_id: []
    )

    result = OrderService.get_order_items(10)

    assert result == []


# ============================================================
# Update Order
# ============================================================

def test_update_order(monkeypatch):
    """Test updating an order."""

    order = Order(
        order_id=1,
        user_id=1,
        total_amount=500.00,
        status="confirmed",
        shipping_address=" Pune "
    )

    monkeypatch.setattr(
        OrderRepository,
        "update_order",
        lambda order: True
    )

    result = OrderService.update_order(order)

    assert result is True
    assert order.shipping_address == "Pune"


def test_update_order_without_id():
    """Test updating order without ID."""

    order = Order(
        order_id=None,
        user_id=1,
        total_amount=500.00,
        status="pending",
        shipping_address="Pune"
    )

    with pytest.raises(ValueError):
        OrderService.update_order(order)


def test_update_order_invalid_user():
    """Test updating order with invalid user."""

    order = Order(
        order_id=1,
        user_id=0,
        total_amount=500.00,
        status="pending",
        shipping_address="Pune"
    )

    with pytest.raises(ValueError):
        OrderService.update_order(order)


def test_update_order_invalid_status():
    """Test updating order with invalid status."""

    order = Order(
        order_id=1,
        user_id=1,
        total_amount=500.00,
        status="invalid",
        shipping_address="Pune"
    )

    with pytest.raises(ValueError):
        OrderService.update_order(order)


def test_update_order_invalid_address():
    """Test updating order with invalid address."""

    order = Order(
        order_id=1,
        user_id=1,
        total_amount=500.00,
        status="pending",
        shipping_address="   "
    )

    with pytest.raises(ValueError):
        OrderService.update_order(order)


def test_update_order_negative_total():
    """Test updating order with negative total."""

    order = Order(
        order_id=1,
        user_id=1,
        total_amount=-500.00,
        status="pending",
        shipping_address="Pune"
    )

    with pytest.raises(ValueError):
        OrderService.update_order(order)


def test_update_order_repository_failure(monkeypatch):
    """Test repository update failure."""

    order = Order(
        order_id=1,
        user_id=1,
        total_amount=500.00,
        status="pending",
        shipping_address="Pune"
    )

    monkeypatch.setattr(
        OrderRepository,
        "update_order",
        lambda order: False
    )

    result = OrderService.update_order(order)

    assert result is False


# ============================================================
# Update Order Status
# ============================================================

def test_update_order_status_invalid_id():
    """Test invalid order ID."""

    with pytest.raises(ValueError):
        OrderService.update_order_status(
            0,
            "pending"
        )


def test_update_order_status_negative_id():
    """Test negative order ID."""

    with pytest.raises(ValueError):
        OrderService.update_order_status(
            -1,
            "pending"
        )


def test_update_order_status_invalid_status():
    """Test invalid status."""

    with pytest.raises(ValueError):
        OrderService.update_order_status(
            1,
            "invalid"
        )


def test_update_order_status_not_found(monkeypatch):
    """Test updating status for missing order."""

    monkeypatch.setattr(
        OrderRepository,
        "get_order_by_id",
        lambda order_id: None
    )

    result = OrderService.update_order_status(
        999,
        "shipped"
    )

    assert result is False


def test_update_order_status(monkeypatch):
    """Test updating order status."""

    order = Order(
        order_id=1,
        user_id=1,
        total_amount=500.00,
        status="pending",
        shipping_address="Pune"
    )

    monkeypatch.setattr(
        OrderRepository,
        "get_order_by_id",
        lambda order_id: order
    )

    monkeypatch.setattr(
        OrderRepository,
        "update_order",
        lambda order: True
    )

    result = OrderService.update_order_status(
        1,
        "shipped"
    )

    assert result is True
    assert order.status == "shipped"


def test_update_order_status_repository_failure(monkeypatch):
    """Test status update repository failure."""

    order = Order(
        order_id=1,
        user_id=1,
        total_amount=500.00,
        status="pending",
        shipping_address="Pune"
    )

    monkeypatch.setattr(
        OrderRepository,
        "get_order_by_id",
        lambda order_id: order
    )

    monkeypatch.setattr(
        OrderRepository,
        "update_order",
        lambda order: False
    )

    result = OrderService.update_order_status(
        1,
        "shipped"
    )

    assert result is False


# ============================================================
# Add Order Item
# ============================================================

def test_add_order_item(monkeypatch):
    """Test adding an order item."""

    item = OrderItem(
        order_item_id=None,
        order_id=1,
        product_id=2,
        quantity=2,
        price=100.00
    )

    monkeypatch.setattr(
        OrderRepository,
        "create_order_item",
        lambda item: item
    )

    result = OrderService.add_order_item(item)

    assert result == item


def test_add_order_item_none_order():
    """Test item with None order ID."""

    item = OrderItem(
        order_id=None,
        product_id=1,
        quantity=1,
        price=100
    )

    with pytest.raises(ValueError):
        OrderService.add_order_item(item)


def test_add_order_item_invalid_order():
    """Test item with invalid order ID."""

    item = OrderItem(
        order_id=0,
        product_id=1,
        quantity=1,
        price=100
    )

    with pytest.raises(ValueError):
        OrderService.add_order_item(item)


def test_add_order_item_none_product():
    """Test item with None product ID."""

    item = OrderItem(
        order_id=1,
        product_id=None,
        quantity=1,
        price=100
    )

    with pytest.raises(ValueError):
        OrderService.add_order_item(item)


def test_add_order_item_invalid_product():
    """Test item with invalid product ID."""

    item = OrderItem(
        order_id=1,
        product_id=0,
        quantity=1,
        price=100
    )

    with pytest.raises(ValueError):
        OrderService.add_order_item(item)


def test_add_order_item_invalid_quantity():
    """Test item with invalid quantity."""

    item = OrderItem(
        order_id=1,
        product_id=1,
        quantity=0,
        price=100
    )

    with pytest.raises(ValueError):
        OrderService.add_order_item(item)


def test_add_order_item_negative_price():
    """Test item with negative price."""

    item = OrderItem(
        order_id=1,
        product_id=1,
        quantity=1,
        price=-100
    )

    with pytest.raises(ValueError):
        OrderService.add_order_item(item)


# ============================================================
# Update Order Item
# ============================================================

def test_update_order_item(monkeypatch):
    """Test updating an order item."""

    item = OrderItem(
        order_item_id=1,
        order_id=1,
        product_id=2,
        quantity=3,
        price=150.00
    )

    monkeypatch.setattr(
        OrderRepository,
        "update_order_item",
        lambda item: True
    )

    result = OrderService.update_order_item(item)

    assert result is True


def test_update_order_item_without_id():
    """Test updating item without ID."""

    item = OrderItem(
        order_item_id=None,
        order_id=1,
        product_id=1,
        quantity=1,
        price=100
    )

    with pytest.raises(ValueError):
        OrderService.update_order_item(item)


def test_update_order_item_none_product():
    """Test updating item with None product ID."""

    item = OrderItem(
        order_item_id=1,
        order_id=1,
        product_id=None,
        quantity=1,
        price=100
    )

    with pytest.raises(ValueError):
        OrderService.update_order_item(item)


def test_update_order_item_invalid_product():
    """Test updating item with invalid product ID."""

    item = OrderItem(
        order_item_id=1,
        order_id=1,
        product_id=0,
        quantity=1,
        price=100
    )

    with pytest.raises(ValueError):
        OrderService.update_order_item(item)


def test_update_order_item_invalid_quantity():
    """Test updating item with invalid quantity."""

    item = OrderItem(
        order_item_id=1,
        order_id=1,
        product_id=1,
        quantity=0,
        price=100
    )

    with pytest.raises(ValueError):
        OrderService.update_order_item(item)


def test_update_order_item_negative_price():
    """Test updating item with negative price."""

    item = OrderItem(
        order_item_id=1,
        order_id=1,
        product_id=1,
        quantity=1,
        price=-100
    )

    with pytest.raises(ValueError):
        OrderService.update_order_item(item)


def test_update_order_item_repository_failure(monkeypatch):
    """Test update order item repository failure."""

    item = OrderItem(
        order_item_id=1,
        order_id=1,
        product_id=1,
        quantity=2,
        price=100
    )

    monkeypatch.setattr(
        OrderRepository,
        "update_order_item",
        lambda item: False
    )

    result = OrderService.update_order_item(item)

    assert result is False


# ============================================================
# Delete Order Item
# ============================================================

def test_delete_order_item_invalid_id():
    """Test invalid order item ID."""

    with pytest.raises(ValueError):
        OrderService.delete_order_item(0)


def test_delete_order_item_negative_id():
    """Test negative order item ID."""

    with pytest.raises(ValueError):
        OrderService.delete_order_item(-1)


def test_delete_order_item_repository_failure(monkeypatch):
    """Test delete order item repository failure."""

    monkeypatch.setattr(
        OrderRepository,
        "delete_order_item",
        lambda order_item_id: False
    )

    result = OrderService.delete_order_item(1)

    assert result is False


# ============================================================
# Delete Order
# ============================================================

def test_delete_order_invalid_id():
    """Test invalid order ID."""

    with pytest.raises(ValueError):
        OrderService.delete_order(0)


def test_delete_order_negative_id():
    """Test negative order ID."""

    with pytest.raises(ValueError):
        OrderService.delete_order(-1)


def test_delete_order(monkeypatch):
    """Test deleting an order."""

    monkeypatch.setattr(
        OrderRepository,
        "delete_order",
        lambda order_id: True
    )

    result = OrderService.delete_order(1)

    assert result is True


def test_delete_order_repository_failure(monkeypatch):
    """Test delete order repository failure."""

    monkeypatch.setattr(
        OrderRepository,
        "delete_order",
        lambda order_id: False
    )

    result = OrderService.delete_order(1)

    assert result is False