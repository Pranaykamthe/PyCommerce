"""
test_order_repository.py
------------------------
Integration and failure-path tests for OrderRepository.

These tests interact with the MySQL database and also
test database connection failure handling.
"""

import uuid
from unittest.mock import patch

import pytest

from models.order import Order
from models.order_item import OrderItem
from models.user import User

from repositories.order_repository import OrderRepository
from repositories.product_repository import ProductRepository
from repositories.user_repository import UserRepository


# ============================================================
# Test User Fixture
# ============================================================

@pytest.fixture(scope="module")
def test_user():
    """
    Create a temporary test user and return its user ID.

    Orders require a valid user_id because of the foreign-key
    relationship between orders and users.
    """

    unique_id = uuid.uuid4().hex[:10]

    user = User(
        name="Order Repository Test",
        email=f"order_repo_{unique_id}@pycommerce.test",
        password="pass12345",
        phone=f"88888{unique_id[:5]}",
        address="Pune",
        role="customer"
    )

    created_user = UserRepository.create(user)

    if created_user is None:
        pytest.fail(
            "Unable to create test user for order repository tests."
        )

    yield created_user.user_id

    # --------------------------------------------------------
    # Cleanup
    # --------------------------------------------------------

    try:
        UserRepository.delete(
            created_user.user_id
        )
    except Exception:
        pass


# ============================================================
# Test Product Fixture
# ============================================================

@pytest.fixture(scope="module")
def test_products():
    """
    Get existing products from the database.

    Order items require valid product IDs because
    order_items.product_id references products.product_id.
    """

    products = ProductRepository.get_all()

    if not products:
        pytest.skip(
            "At least one product is required "
            "for order repository tests."
        )

    if len(products) == 1:
        return products[0], products[0]

    return products[0], products[1]


# ============================================================
# Order Tests
# ============================================================

def test_create_order(test_user):
    """Test creating an order in MySQL."""

    order = Order(
        user_id=test_user,
        total_amount=1500.00,
        status="pending",
        shipping_address="Pune"
    )

    created_order = OrderRepository.create_order(
        order
    )

    assert created_order is not None
    assert created_order.order_id is not None

    order_id = created_order.order_id

    saved_order = OrderRepository.get_order_by_id(
        order_id
    )

    assert saved_order is not None
    assert saved_order.order_id == order_id
    assert saved_order.user_id == test_user
    assert saved_order.total_amount == 1500.00
    assert saved_order.status == "pending"
    assert saved_order.shipping_address == "Pune"

    OrderRepository.delete_order(
        order_id
    )


def test_get_order_by_id(test_user):
    """Test retrieving an order by ID."""

    order = Order(
        user_id=test_user,
        total_amount=750.00,
        status="pending",
        shipping_address="Mumbai"
    )

    created_order = OrderRepository.create_order(
        order
    )

    assert created_order is not None
    assert created_order.order_id is not None

    order_id = created_order.order_id

    retrieved_order = OrderRepository.get_order_by_id(
        order_id
    )

    assert retrieved_order is not None
    assert retrieved_order.order_id == order_id
    assert retrieved_order.user_id == test_user
    assert retrieved_order.total_amount == 750.00
    assert retrieved_order.status == "pending"
    assert retrieved_order.shipping_address == "Mumbai"

    OrderRepository.delete_order(
        order_id
    )


def test_get_order_not_found():
    """Test retrieving a non-existing order."""

    result = OrderRepository.get_order_by_id(
        999999999
    )

    assert result is None


def test_get_orders_by_user(test_user):
    """Test retrieving all orders for a user."""

    order = Order(
        user_id=test_user,
        total_amount=900.00,
        status="pending",
        shipping_address="Pune"
    )

    created_order = OrderRepository.create_order(
        order
    )

    assert created_order is not None

    orders = OrderRepository.get_orders_by_user(
        test_user
    )

    assert isinstance(orders, list)
    assert len(orders) >= 1

    found_order = next(
        (
            item
            for item in orders
            if item.order_id == created_order.order_id
        ),
        None
    )

    assert found_order is not None
    assert found_order.user_id == test_user
    assert found_order.total_amount == 900.00

    OrderRepository.delete_order(
        created_order.order_id
    )


def test_get_orders_by_user_not_found():
    """Test retrieving orders for a user with no orders."""

    orders = OrderRepository.get_orders_by_user(
        999999999
    )

    assert orders == []


# ============================================================
# Get All Orders
# ============================================================

def test_get_all_orders(test_user):
    """Test retrieving all orders."""

    order_1 = Order(
        user_id=test_user,
        total_amount=500.00,
        status="pending",
        shipping_address="Pune"
    )

    order_2 = Order(
        user_id=test_user,
        total_amount=750.00,
        status="confirmed",
        shipping_address="Mumbai"
    )

    created_order_1 = OrderRepository.create_order(
        order_1
    )

    created_order_2 = OrderRepository.create_order(
        order_2
    )

    assert created_order_1 is not None
    assert created_order_2 is not None

    orders = OrderRepository.get_all_orders()

    assert isinstance(orders, list)

    order_ids = [
        order.order_id
        for order in orders
    ]

    assert created_order_1.order_id in order_ids
    assert created_order_2.order_id in order_ids

    OrderRepository.delete_order(
        created_order_1.order_id
    )

    OrderRepository.delete_order(
        created_order_2.order_id
    )


def test_get_all_orders_not_found():
    """
    Test get_all_orders when the database contains no
    matching records.

    The repository should return a list even when there
    are no orders.
    """

    result = OrderRepository.get_all_orders()

    assert isinstance(result, list)


# ============================================================
# Update Order
# ============================================================

def test_update_order(test_user):
    """Test updating an existing order."""

    order = Order(
        user_id=test_user,
        total_amount=1000.00,
        status="pending",
        shipping_address="Pune"
    )

    created_order = OrderRepository.create_order(
        order
    )

    assert created_order is not None
    assert created_order.order_id is not None

    created_order.total_amount = 1500.00
    created_order.status = "confirmed"
    created_order.shipping_address = "Mumbai"

    result = OrderRepository.update_order(
        created_order
    )

    assert result is True

    updated_order = OrderRepository.get_order_by_id(
        created_order.order_id
    )

    assert updated_order is not None
    assert updated_order.total_amount == 1500.00
    assert updated_order.status == "confirmed"
    assert updated_order.shipping_address == "Mumbai"

    OrderRepository.delete_order(
        created_order.order_id
    )


def test_update_order_without_id(test_user):
    """Test updating an order without an ID."""

    order = Order(
        user_id=test_user,
        total_amount=500.00,
        status="pending",
        shipping_address="Pune"
    )

    result = OrderRepository.update_order(
        order
    )

    assert result is False


def test_update_order_status(test_user):
    """Test updating the order status."""

    order = Order(
        user_id=test_user,
        total_amount=800.00,
        status="pending",
        shipping_address="Pune"
    )

    created_order = OrderRepository.create_order(
        order
    )

    assert created_order is not None

    created_order.status = "shipped"

    result = OrderRepository.update_order(
        created_order
    )

    assert result is True

    updated_order = OrderRepository.get_order_by_id(
        created_order.order_id
    )

    assert updated_order is not None
    assert updated_order.status == "shipped"

    OrderRepository.delete_order(
        created_order.order_id
    )


# ============================================================
# Order Item Tests
# ============================================================

def test_create_order_item(
    test_user,
    test_products
):
    """Test creating an order item."""

    product_1, _ = test_products

    order = Order(
        user_id=test_user,
        total_amount=500.00,
        status="pending",
        shipping_address="Pune"
    )

    created_order = OrderRepository.create_order(
        order
    )

    assert created_order is not None

    order_item = OrderItem(
        order_id=created_order.order_id,
        product_id=product_1.product_id,
        quantity=2,
        price=250.00
    )

    created_item = OrderRepository.create_order_item(
        order_item
    )

    assert created_item is not None
    assert created_item.order_item_id is not None
    assert created_item.order_id == created_order.order_id
    assert created_item.product_id == product_1.product_id
    assert created_item.quantity == 2
    assert created_item.price == 250.00

    OrderRepository.delete_order(
        created_order.order_id
    )


def test_get_order_items(
    test_user,
    test_products
):
    """Test retrieving all items belonging to an order."""

    product_1, _ = test_products

    order = Order(
        user_id=test_user,
        total_amount=600.00,
        status="pending",
        shipping_address="Pune"
    )

    created_order = OrderRepository.create_order(
        order
    )

    assert created_order is not None

    order_item = OrderItem(
        order_id=created_order.order_id,
        product_id=product_1.product_id,
        quantity=2,
        price=300.00
    )

    created_item = OrderRepository.create_order_item(
        order_item
    )

    assert created_item is not None

    items = OrderRepository.get_order_items(
        created_order.order_id
    )

    assert isinstance(items, list)
    assert len(items) >= 1

    found_item = next(
        (
            item
            for item in items
            if item.order_item_id == created_item.order_item_id
        ),
        None
    )

    assert found_item is not None
    assert found_item.product_id == product_1.product_id
    assert found_item.quantity == 2
    assert found_item.price == 300.00

    OrderRepository.delete_order(
        created_order.order_id
    )


def test_get_order_item_by_id(
    test_user,
    test_products
):
    """Test retrieving an order item by ID."""

    product_1, _ = test_products

    order = Order(
        user_id=test_user,
        total_amount=400.00,
        status="pending",
        shipping_address="Pune"
    )

    created_order = OrderRepository.create_order(
        order
    )

    assert created_order is not None

    order_item = OrderItem(
        order_id=created_order.order_id,
        product_id=product_1.product_id,
        quantity=2,
        price=200.00
    )

    created_item = OrderRepository.create_order_item(
        order_item
    )

    assert created_item is not None
    assert created_item.order_item_id is not None

    retrieved_item = OrderRepository.get_order_item_by_id(
        created_item.order_item_id
    )

    assert retrieved_item is not None
    assert (
        retrieved_item.order_item_id
        == created_item.order_item_id
    )
    assert retrieved_item.order_id == created_order.order_id
    assert retrieved_item.product_id == product_1.product_id
    assert retrieved_item.quantity == 2
    assert retrieved_item.price == 200.00

    OrderRepository.delete_order(
        created_order.order_id
    )


def test_get_order_item_not_found():
    """Test retrieving a non-existing order item."""

    result = OrderRepository.get_order_item_by_id(
        999999999
    )

    assert result is None


def test_update_order_item(
    test_user,
    test_products
):
    """Test updating an existing order item."""

    product_1, product_2 = test_products

    order = Order(
        user_id=test_user,
        total_amount=500.00,
        status="pending",
        shipping_address="Pune"
    )

    created_order = OrderRepository.create_order(
        order
    )

    assert created_order is not None

    order_item = OrderItem(
        order_id=created_order.order_id,
        product_id=product_1.product_id,
        quantity=2,
        price=250.00
    )

    created_item = OrderRepository.create_order_item(
        order_item
    )

    assert created_item is not None
    assert created_item.order_item_id is not None

    created_item.quantity = 3
    created_item.price = 300.00

    if product_2.product_id != product_1.product_id:
        created_item.product_id = product_2.product_id

    result = OrderRepository.update_order_item(
        created_item
    )

    assert result is True

    updated_item = (
        OrderRepository.get_order_item_by_id(
            created_item.order_item_id
        )
    )

    assert updated_item is not None
    assert updated_item.quantity == 3
    assert updated_item.price == 300.00

    expected_product_id = (
        product_2.product_id
        if product_2.product_id != product_1.product_id
        else product_1.product_id
    )

    assert (
        updated_item.product_id
        == expected_product_id
    )

    OrderRepository.delete_order(
        created_order.order_id
    )


def test_update_order_item_without_id():
    """Test updating an order item without an ID."""

    order_item = OrderItem(
        order_id=1,
        product_id=1,
        quantity=2,
        price=100.00
    )

    result = OrderRepository.update_order_item(
        order_item
    )

    assert result is False


def test_delete_order_item(
    test_user,
    test_products
):
    """Test deleting an order item."""

    product_1, _ = test_products

    order = Order(
        user_id=test_user,
        total_amount=500.00,
        status="pending",
        shipping_address="Pune"
    )

    created_order = OrderRepository.create_order(
        order
    )

    assert created_order is not None

    order_item = OrderItem(
        order_id=created_order.order_id,
        product_id=product_1.product_id,
        quantity=2,
        price=250.00
    )

    created_item = OrderRepository.create_order_item(
        order_item
    )

    assert created_item is not None

    result = OrderRepository.delete_order_item(
        created_item.order_item_id
    )

    assert result is True

    deleted_item = (
        OrderRepository.get_order_item_by_id(
            created_item.order_item_id
        )
    )

    assert deleted_item is None

    OrderRepository.delete_order(
        created_order.order_id
    )


def test_delete_order_item_not_found():
    """Test deleting a non-existing order item."""

    result = OrderRepository.delete_order_item(
        999999999
    )

    assert result is False


# ============================================================
# Delete Order
# ============================================================

def test_delete_order(
    test_user,
    test_products
):
    """Test deleting an order and its items."""

    product_1, _ = test_products

    order = Order(
        user_id=test_user,
        total_amount=500.00,
        status="pending",
        shipping_address="Pune"
    )

    created_order = OrderRepository.create_order(
        order
    )

    assert created_order is not None

    order_item = OrderItem(
        order_id=created_order.order_id,
        product_id=product_1.product_id,
        quantity=2,
        price=250.00
    )

    created_item = OrderRepository.create_order_item(
        order_item
    )

    assert created_item is not None

    result = OrderRepository.delete_order(
        created_order.order_id
    )

    assert result is True

    deleted_order = OrderRepository.get_order_by_id(
        created_order.order_id
    )

    assert deleted_order is None

    deleted_items = OrderRepository.get_order_items(
        created_order.order_id
    )

    assert deleted_items == []


def test_delete_order_not_found():
    """Test deleting a non-existing order."""

    result = OrderRepository.delete_order(
        999999999
    )

    assert result is False


# ============================================================
# Connection Failure Tests
# ============================================================

def test_create_order_connection_failure():
    """Test create_order when database connection fails."""

    order = Order(
        user_id=1,
        total_amount=500.00,
        status="pending",
        shipping_address="Pune"
    )

    with patch(
        "repositories.order_repository.get_connection",
        return_value=None
    ):
        result = OrderRepository.create_order(
            order
        )

    assert result is None


def test_get_order_by_id_connection_failure():
    """Test get_order_by_id when database connection fails."""

    with patch(
        "repositories.order_repository.get_connection",
        return_value=None
    ):
        result = OrderRepository.get_order_by_id(
            1
        )

    assert result is None


def test_get_orders_by_user_connection_failure():
    """Test get_orders_by_user when database connection fails."""

    with patch(
        "repositories.order_repository.get_connection",
        return_value=None
    ):
        result = OrderRepository.get_orders_by_user(
            1
        )

    assert result == []


def test_get_all_orders_connection_failure():
    """Test get_all_orders when database connection fails."""

    with patch(
        "repositories.order_repository.get_connection",
        return_value=None
    ):
        result = OrderRepository.get_all_orders()

    assert result == []


def test_update_order_connection_failure():
    """Test update_order when database connection fails."""

    order = Order(
        order_id=1,
        user_id=1,
        total_amount=500.00,
        status="pending",
        shipping_address="Pune"
    )

    with patch(
        "repositories.order_repository.get_connection",
        return_value=None
    ):
        result = OrderRepository.update_order(
            order
        )

    assert result is False


def test_create_order_item_connection_failure():
    """Test create_order_item when database connection fails."""

    order_item = OrderItem(
        order_id=1,
        product_id=1,
        quantity=2,
        price=250.00
    )

    with patch(
        "repositories.order_repository.get_connection",
        return_value=None
    ):
        result = OrderRepository.create_order_item(
            order_item
        )

    assert result is None


def test_get_order_item_by_id_connection_failure():
    """Test get_order_item_by_id when database connection fails."""

    with patch(
        "repositories.order_repository.get_connection",
        return_value=None
    ):
        result = OrderRepository.get_order_item_by_id(
            1
        )

    assert result is None


def test_get_order_items_connection_failure():
    """Test get_order_items when database connection fails."""

    with patch(
        "repositories.order_repository.get_connection",
        return_value=None
    ):
        result = OrderRepository.get_order_items(
            1
        )

    assert result == []


def test_update_order_item_connection_failure():
    """Test update_order_item when database connection fails."""

    order_item = OrderItem(
        order_item_id=1,
        order_id=1,
        product_id=1,
        quantity=2,
        price=250.00
    )

    with patch(
        "repositories.order_repository.get_connection",
        return_value=None
    ):
        result = OrderRepository.update_order_item(
            order_item
        )

    assert result is False


def test_delete_order_item_connection_failure():
    """Test delete_order_item when database connection fails."""

    with patch(
        "repositories.order_repository.get_connection",
        return_value=None
    ):
        result = OrderRepository.delete_order_item(
            1
        )

    assert result is False


def test_delete_order_connection_failure():
    """Test delete_order when database connection fails."""

    with patch(
        "repositories.order_repository.get_connection",
        return_value=None
    ):
        result = OrderRepository.delete_order(
            1
        )

    assert result is False