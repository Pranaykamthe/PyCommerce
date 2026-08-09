"""
Tests for OrderRepository.
"""

from uuid import uuid4

from models.order import Order
from models.order_item import OrderItem
from models.user import User

from repositories.order_repository import OrderRepository
from repositories.user_repository import UserRepository


# ============================================================
# Test Data Helpers
# ============================================================

def create_test_user() -> User:
    """Create a unique test user."""

    unique_id = uuid4().hex[:8]

    user = User(
        name="Order Repository Test",
        email=f"order_repo_{unique_id}@pycommerce.test",
        password="pass12345",
        phone=f"88888{unique_id[:5]}",
        address="Pune",
        role="customer"
    )

    created_user = UserRepository.create(user)

    assert created_user is not None
    assert created_user.user_id is not None

    return created_user


def create_test_order() -> Order:
    """Create a unique test order."""

    user = create_test_user()

    order = Order(
        user_id=user.user_id,
        total_amount=1000.00,
        status="pending",
        shipping_address="Pune"
    )

    created_order = OrderRepository.create_order(order)

    assert created_order is not None
    assert created_order.order_id is not None

    return created_order


def create_test_order_item(
    order_id: int
) -> OrderItem:
    """Create a test order item."""

    return OrderItem(
        order_id=order_id,
        product_id=278,
        quantity=2,
        price=500.00
    )


# ============================================================
# Create Order
# ============================================================

def test_create_order():
    """Test creating an order."""

    order = create_test_order()

    assert order is not None
    assert order.order_id is not None
    assert order.user_id is not None
    assert order.total_amount == 1000.00
    assert order.status == "pending"
    assert order.shipping_address == "Pune"


# ============================================================
# Get Order By ID
# ============================================================

def test_get_order_by_id():
    """Test retrieving an order by ID."""

    created = create_test_order()

    found = OrderRepository.get_order_by_id(
        created.order_id
    )

    assert found is not None
    assert found.order_id == created.order_id
    assert found.user_id == created.user_id
    assert found.total_amount == 1000.00
    assert found.status == "pending"
    assert found.shipping_address == "Pune"


# ============================================================
# Get Order Not Found
# ============================================================

def test_get_order_not_found():
    """Test retrieving a nonexistent order."""

    order = OrderRepository.get_order_by_id(
        999999999
    )

    assert order is None


# ============================================================
# Get Orders By User
# ============================================================

def test_get_orders_by_user():
    """Test retrieving orders belonging to a user."""

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

    orders = OrderRepository.get_orders_by_user(
        user.user_id
    )

    assert isinstance(orders, list)

    order_ids = [
        order.order_id
        for order in orders
    ]

    assert created1.order_id in order_ids
    assert created2.order_id in order_ids


# ============================================================
# Get Orders By User - Not Found
# ============================================================

def test_get_orders_by_user_not_found():
    """Test retrieving orders for a user with no orders."""

    user = create_test_user()

    orders = OrderRepository.get_orders_by_user(
        user.user_id
    )

    assert isinstance(orders, list)
    assert orders == []


# ============================================================
# Update Order
# ============================================================

def test_update_order():
    """Test updating an existing order."""

    created = create_test_order()

    created.total_amount = 1500.00
    created.status = "confirmed"
    created.shipping_address = "Mumbai"

    result = OrderRepository.update_order(
        created
    )

    assert result is True

    updated = OrderRepository.get_order_by_id(
        created.order_id
    )

    assert updated is not None
    assert updated.total_amount == 1500.00
    assert updated.status == "confirmed"
    assert updated.shipping_address == "Mumbai"


# ============================================================
# Update Order Without ID
# ============================================================

def test_update_order_without_id():
    """Test updating an order without an order ID."""

    order = Order(
        user_id=1,
        total_amount=500.00,
        status="pending",
        shipping_address="Pune"
    )

    result = OrderRepository.update_order(
        order
    )

    assert result is False


# ============================================================
# Update Order Status
# ============================================================

def test_update_order_status():
    """Test updating order status."""

    created = create_test_order()

    result = OrderRepository.update_order(
        Order(
            order_id=created.order_id,
            user_id=created.user_id,
            total_amount=created.total_amount,
            status="shipped",
            shipping_address=created.shipping_address
        )
    )

    assert result is True

    updated = OrderRepository.get_order_by_id(
        created.order_id
    )

    assert updated is not None
    assert updated.status == "shipped"


# ============================================================
# Create Order Item
# ============================================================

def test_create_order_item():
    """Test creating an order item."""

    order = create_test_order()

    item = create_test_order_item(
        order.order_id
    )

    created = OrderRepository.create_order_item(
        item
    )

    assert created is not None
    assert created.order_item_id is not None
    assert created.order_id == order.order_id
    assert created.product_id == 278
    assert created.quantity == 2
    assert created.price == 500.00


# ============================================================
# Get Order Items
# ============================================================

def test_get_order_items():
    """Test retrieving items belonging to an order."""

    order = create_test_order()

    item = create_test_order_item(
        order.order_id
    )

    created = OrderRepository.create_order_item(
        item
    )

    assert created is not None

    items = OrderRepository.get_order_items(
        order.order_id
    )

    assert isinstance(items, list)

    item_ids = [
        item.order_item_id
        for item in items
    ]

    assert created.order_item_id in item_ids


# ============================================================
# Get Order Item By ID
# ============================================================

def test_get_order_item_by_id():
    """Test retrieving an order item by ID."""

    order = create_test_order()

    item = create_test_order_item(
        order.order_id
    )

    created = OrderRepository.create_order_item(
        item
    )

    assert created is not None
    assert created.order_item_id is not None

    found = OrderRepository.get_order_item_by_id(
        created.order_item_id
    )

    assert found is not None
    assert found.order_item_id == created.order_item_id
    assert found.order_id == order.order_id
    assert found.product_id == 278
    assert found.quantity == 2
    assert found.price == 500.00


# ============================================================
# Get Order Item Not Found
# ============================================================

def test_get_order_item_not_found():
    """Test retrieving a nonexistent order item."""

    item = OrderRepository.get_order_item_by_id(
        999999999
    )

    assert item is None


# ============================================================
# Update Order Item
# ============================================================

def test_update_order_item():
    """Test updating an existing order item."""

    order = create_test_order()

    item = create_test_order_item(
        order.order_id
    )

    created = OrderRepository.create_order_item(
        item
    )

    assert created is not None
    assert created.order_item_id is not None

    created.quantity = 3
    created.price = 600.00

    result = OrderRepository.update_order_item(
        created
    )

    assert result is True

    updated = OrderRepository.get_order_item_by_id(
        created.order_item_id
    )

    assert updated is not None
    assert updated.quantity == 3
    assert updated.price == 600.00


# ============================================================
# Update Order Item Without ID
# ============================================================

def test_update_order_item_without_id():
    """Test updating an order item without ID."""

    item = OrderItem(
        order_id=1,
        product_id=278,
        quantity=2,
        price=500.00
    )

    result = OrderRepository.update_order_item(
        item
    )

    assert result is False


# ============================================================
# Delete Order Item
# ============================================================

def test_delete_order_item():
    """Test deleting an order item."""

    order = create_test_order()

    item = create_test_order_item(
        order.order_id
    )

    created = OrderRepository.create_order_item(
        item
    )

    assert created is not None
    assert created.order_item_id is not None

    result = OrderRepository.delete_order_item(
        created.order_item_id
    )

    assert result is True

    deleted = OrderRepository.get_order_item_by_id(
        created.order_item_id
    )

    assert deleted is None


# ============================================================
# Delete Order Item Not Found
# ============================================================

def test_delete_order_item_not_found():
    """Test deleting a nonexistent order item."""

    result = OrderRepository.delete_order_item(
        999999999
    )

    assert result is False


# ============================================================
# Delete Order
# ============================================================

def test_delete_order():
    """Test deleting an order."""

    order = create_test_order()

    result = OrderRepository.delete_order(
        order.order_id
    )

    assert result is True

    deleted = OrderRepository.get_order_by_id(
        order.order_id
    )

    assert deleted is None


# ============================================================
# Delete Order Not Found
# ============================================================

def test_delete_order_not_found():
    """Test deleting a nonexistent order."""

    result = OrderRepository.delete_order(
        999999999
    )

    assert result is False