"""
Tests for OrderService.
"""

from uuid import uuid4

from models.order_item import OrderItem
from models.order import Order
from models.user import User

from repositories.user_repository import UserRepository
from repositories.order_repository import OrderRepository

from services.order_service import OrderService


# ============================================================
# Test Data Helpers
# ============================================================

def create_test_user() -> User:
    """Create a unique test user."""

    unique_id = uuid4().hex[:8]

    user = User(
        name="Order Service Test",
        email=f"order_service_{unique_id}@pycommerce.test",
        password="pass12345",
        phone=f"77777{unique_id[:5]}",
        address="Pune",
        role="customer"
    )

    created = UserRepository.create(user)

    assert created is not None
    assert created.user_id is not None

    return created


# ============================================================
# Get Order
# ============================================================

def test_get_order():
    """Test retrieving an order."""

    user = create_test_user()

    order = Order(
        user_id=user.user_id,
        total_amount=1200.00,
        status="pending",
        shipping_address="Pune"
    )

    created_order = OrderRepository.create_order(order)

    assert created_order is not None
    assert created_order.order_id is not None

    found = OrderService.get_order(
        created_order.order_id
    )

    assert found is not None
    assert found.order_id == created_order.order_id
    assert found.user_id == created_order.user_id
    assert found.total_amount == created_order.total_amount
    assert found.status == created_order.status


# ============================================================
# Get Order Not Found
# ============================================================

def test_get_order_not_found():
    """Test retrieving a nonexistent order."""

    result = OrderService.get_order(
        999999999
    )

    assert result is None


# ============================================================
# Get User Orders
# ============================================================

def test_get_user_orders():
    """Test retrieving all orders for a user."""

    user = create_test_user()

    order1 = Order(
        user_id=user.user_id,
        total_amount=500.00,
        status="pending",
        shipping_address="Pune"
    )

    order2 = Order(
        user_id=user.user_id,
        total_amount=750.00,
        status="confirmed",
        shipping_address="Mumbai"
    )

    created1 = OrderRepository.create_order(order1)
    created2 = OrderRepository.create_order(order2)

    assert created1 is not None
    assert created2 is not None

    orders = OrderService.get_user_orders(
        user.user_id
    )

    assert isinstance(orders, list)

    order_ids = [
        item.order_id
        for item in orders
    ]

    assert created1.order_id in order_ids
    assert created2.order_id in order_ids


# ============================================================
# Get User Orders - Empty
# ============================================================

def test_get_user_orders_empty():
    """Test retrieving orders for a user with no orders."""

    user = create_test_user()

    orders = OrderService.get_user_orders(
        user.user_id
    )

    assert isinstance(orders, list)
    assert orders == []


# ============================================================
# Create Order
# ============================================================

def test_create_order():
    """Test creating an order through the service."""

    user = create_test_user()

    order = Order(
        user_id=user.user_id,
        total_amount=1200.00,
        status="pending",
        shipping_address="Pune"
    )

    items = [
        OrderItem(
            product_id=278,
            quantity=1,
            price=1200.00
        )
    ]

    created = OrderService.create_order(
        order,
        items
    )

    assert created is not None
    assert created.order_id is not None
    assert created.user_id == user.user_id
    assert created.total_amount == 1200.00
    assert created.status == "pending"


# ============================================================
# Create Order Invalid User
# ============================================================

def test_create_order_invalid_user():
    """Test creating an order for a nonexistent user."""

    order = Order(
        user_id=999999999,
        total_amount=500.00,
        status="pending",
        shipping_address="Pune"
    )

    items = []

    try:
        result = OrderService.create_order(
            order,
            items
        )

        assert result is None

    except ValueError:
        assert True


# ============================================================
# Update Order Status
# ============================================================

def test_update_order_status():
    """Test updating order status."""

    user = create_test_user()

    order = Order(
        user_id=user.user_id,
        total_amount=1200.00,
        status="pending",
        shipping_address="Pune"
    )

    created_order = OrderRepository.create_order(order)

    assert created_order is not None

    result = OrderService.update_order_status(
        order_id=created_order.order_id,
        status="confirmed"
    )

    assert result is True

    updated = OrderService.get_order(
        created_order.order_id
    )

    assert updated is not None
    assert updated.status == "confirmed"


# ============================================================
# Update Order Status - Invalid Status
# ============================================================

def test_update_order_status_invalid():
    """Test updating order with an invalid status."""

    user = create_test_user()

    order = Order(
        user_id=user.user_id,
        total_amount=1200.00,
        status="pending",
        shipping_address="Pune"
    )

    created_order = OrderRepository.create_order(order)

    assert created_order is not None

    try:
        result = OrderService.update_order_status(
            order_id=created_order.order_id,
            status="invalid_status"
        )

        assert result is False

    except ValueError:
        assert True


# ============================================================
# Update Order Not Found
# ============================================================

def test_update_order_not_found():
    """Test updating a nonexistent order."""

    try:
        result = OrderService.update_order_status(
            order_id=999999999,
            status="confirmed"
        )

        assert result is False

    except ValueError:
        assert True


# ============================================================
# Delete Order
# ============================================================

def test_delete_order():
    """Test deleting an order."""

    user = create_test_user()

    order = Order(
        user_id=user.user_id,
        total_amount=1200.00,
        status="pending",
        shipping_address="Pune"
    )

    created_order = OrderRepository.create_order(order)

    assert created_order is not None

    result = OrderService.delete_order(
        created_order.order_id
    )

    assert result is True

    deleted = OrderService.get_order(
        created_order.order_id
    )

    assert deleted is None


# ============================================================
# Delete Order Not Found
# ============================================================

def test_delete_order_not_found():
    """Test deleting a nonexistent order."""

    result = OrderService.delete_order(
        999999999
    )

    assert result is False


# ============================================================
# Get Order Items
# ============================================================

def test_get_order_items():
    """Test retrieving order items."""

    user = create_test_user()

    order = Order(
        user_id=user.user_id,
        total_amount=1200.00,
        status="pending",
        shipping_address="Pune"
    )

    created_order = OrderRepository.create_order(order)

    assert created_order is not None

    items = OrderService.get_order_items(
        created_order.order_id
    )

    assert isinstance(items, list)


# ============================================================
# Get Order Items - Invalid Order
# ============================================================

def test_get_order_items_invalid_order():
    """Test retrieving items for nonexistent order."""

    try:
        items = OrderService.get_order_items(
            999999999
        )

        assert isinstance(items, list)

    except ValueError:
        assert True