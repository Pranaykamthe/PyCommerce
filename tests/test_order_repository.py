"""
test_order_repository.py
------------------------
Integration tests for OrderRepository.
"""

import uuid

from models.order import Order
from models.order_item import OrderItem
from models.product import Product
from models.user import User

from repositories.order_repository import OrderRepository
from repositories.product_repository import ProductRepository
from repositories.user_repository import UserRepository
from services.auth_service import AuthService


def create_test_user() -> User:
    """Create a temporary test user."""

    email = (
        f"order_test_{uuid.uuid4().hex[:10]}"
        "@pycommerce.test"
    )

    return User(
        name="Order Test User",
        email=email,
        password=AuthService.hash_password(
            "TestPassword123"
        ),
        phone="9999999999",
        address="Test Address",
        role="customer"
    )


def create_test_product() -> Product:
    """Create a temporary test product."""

    return Product(
        category_id=1,
        name=f"Order Test Product "
             f"{uuid.uuid4().hex[:8]}",
        description="Temporary order test product",
        price=500.00,
        stock=10,
        image_url="order-test.jpg"
    )


def test_create_order():
    """Test creating an order."""

    user = UserRepository.create(
        create_test_user()
    )

    assert user is not None
    assert user.user_id is not None

    order = Order(
        user_id=user.user_id,
        total_amount=1000.00,
        status="pending",
        shipping_address="Test Address"
    )

    created_order = OrderRepository.create_order(
        order
    )

    assert created_order is not None
    assert created_order.order_id is not None
    assert created_order.user_id == user.user_id
    assert created_order.total_amount == 1000.00
    assert created_order.status == "pending"

    OrderRepository.delete_order(
        created_order.order_id
    )

    UserRepository.delete(
        user.user_id
    )


def test_get_order_by_id():
    """Test retrieving an order by ID."""

    user = UserRepository.create(
        create_test_user()
    )

    assert user is not None

    order = Order(
        user_id=user.user_id,
        total_amount=750.00,
        status="pending",
        shipping_address="Test Address"
    )

    created_order = OrderRepository.create_order(
        order
    )

    assert created_order is not None

    retrieved_order = OrderRepository.get_order_by_id(
        created_order.order_id
    )

    assert retrieved_order is not None
    assert retrieved_order.order_id == (
        created_order.order_id
    )
    assert retrieved_order.user_id == user.user_id

    OrderRepository.delete_order(
        created_order.order_id
    )

    UserRepository.delete(
        user.user_id
    )


def test_get_orders_by_user():
    """Test retrieving orders belonging to a user."""

    user = UserRepository.create(
        create_test_user()
    )

    assert user is not None

    order = Order(
        user_id=user.user_id,
        total_amount=300.00,
        status="pending",
        shipping_address="Test Address"
    )

    created_order = OrderRepository.create_order(
        order
    )

    assert created_order is not None

    orders = OrderRepository.get_orders_by_user(
        user.user_id
    )

    assert isinstance(orders, list)
    assert len(orders) >= 1

    found = any(
        item.order_id == created_order.order_id
        for item in orders
    )

    assert found is True

    OrderRepository.delete_order(
        created_order.order_id
    )

    UserRepository.delete(
        user.user_id
    )


def test_update_order():
    """Test updating an order."""

    user = UserRepository.create(
        create_test_user()
    )

    assert user is not None

    order = Order(
        user_id=user.user_id,
        total_amount=500.00,
        status="pending",
        shipping_address="Old Address"
    )

    created_order = OrderRepository.create_order(
        order
    )

    assert created_order is not None

    created_order.total_amount = 750.00
    created_order.status = "confirmed"
    created_order.shipping_address = "New Address"

    result = OrderRepository.update_order(
        created_order
    )

    assert result is True

    updated_order = OrderRepository.get_order_by_id(
        created_order.order_id
    )

    assert updated_order is not None
    assert updated_order.total_amount == 750.00
    assert updated_order.status == "confirmed"
    assert updated_order.shipping_address == (
        "New Address"
    )

    OrderRepository.delete_order(
        created_order.order_id
    )

    UserRepository.delete(
        user.user_id
    )


def test_update_order_without_id():
    """Test updating an order without an ID."""

    order = Order(
        order_id=None,
        user_id=1,
        total_amount=100.00,
        status="pending",
        shipping_address="Test"
    )

    result = OrderRepository.update_order(
        order
    )

    assert result is False


def test_create_order_item():
    """Test creating an order item."""

    user = UserRepository.create(
        create_test_user()
    )

    assert user is not None

    product = ProductRepository.create(
        create_test_product()
    )

    assert product is not None
    assert product.product_id is not None

    order = Order(
        user_id=user.user_id,
        total_amount=1000.00,
        status="pending",
        shipping_address="Test Address"
    )

    created_order = OrderRepository.create_order(
        order
    )

    assert created_order is not None

    order_item = OrderItem(
        order_id=created_order.order_id,
        product_id=product.product_id,
        quantity=2,
        price=500.00
    )

    created_item = (
        OrderRepository.create_order_item(
            order_item
        )
    )

    assert created_item is not None
    assert created_item.order_item_id is not None

    retrieved_item = (
        OrderRepository.get_order_item_by_id(
            created_item.order_item_id
        )
    )

    assert retrieved_item is not None
    assert retrieved_item.order_id == (
        created_order.order_id
    )
    assert retrieved_item.product_id == (
        product.product_id
    )
    assert retrieved_item.quantity == 2
    assert retrieved_item.price == 500.00

    OrderRepository.delete_order(
        created_order.order_id
    )

    ProductRepository.delete(
        product.product_id
    )

    UserRepository.delete(
        user.user_id
    )


def test_get_order_items():
    """Test retrieving all items for an order."""

    user = UserRepository.create(
        create_test_user()
    )

    assert user is not None

    product = ProductRepository.create(
        create_test_product()
    )

    assert product is not None

    order = Order(
        user_id=user.user_id,
        total_amount=1000.00,
        status="pending",
        shipping_address="Test Address"
    )

    created_order = OrderRepository.create_order(
        order
    )

    assert created_order is not None

    item = OrderItem(
        order_id=created_order.order_id,
        product_id=product.product_id,
        quantity=2,
        price=500.00
    )

    OrderRepository.create_order_item(
        item
    )

    items = OrderRepository.get_order_items(
        created_order.order_id
    )

    assert isinstance(items, list)
    assert len(items) == 1
    assert items[0].quantity == 2
    assert items[0].price == 500.00

    OrderRepository.delete_order(
        created_order.order_id
    )

    ProductRepository.delete(
        product.product_id
    )

    UserRepository.delete(
        user.user_id
    )


def test_update_order_item():
    """Test updating an order item."""

    user = UserRepository.create(
        create_test_user()
    )

    assert user is not None

    product = ProductRepository.create(
        create_test_product()
    )

    assert product is not None

    order = Order(
        user_id=user.user_id,
        total_amount=500.00,
        status="pending",
        shipping_address="Test Address"
    )

    created_order = OrderRepository.create_order(
        order
    )

    assert created_order is not None

    item = OrderItem(
        order_id=created_order.order_id,
        product_id=product.product_id,
        quantity=1,
        price=500.00
    )

    created_item = (
        OrderRepository.create_order_item(item)
    )

    assert created_item is not None

    created_item.quantity = 3
    created_item.price = 450.00

    result = (
        OrderRepository.update_order_item(
            created_item
        )
    )

    assert result is True

    updated_item = (
        OrderRepository.get_order_item_by_id(
            created_item.order_item_id
        )
    )

    assert updated_item is not None
    assert updated_item.quantity == 3
    assert updated_item.price == 450.00

    OrderRepository.delete_order(
        created_order.order_id
    )

    ProductRepository.delete(
        product.product_id
    )

    UserRepository.delete(
        user.user_id
    )


def test_delete_order_item():
    """Test deleting an order item."""

    user = UserRepository.create(
        create_test_user()
    )

    assert user is not None

    product = ProductRepository.create(
        create_test_product()
    )

    assert product is not None

    order = Order(
        user_id=user.user_id,
        total_amount=500.00,
        status="pending",
        shipping_address="Test Address"
    )

    created_order = OrderRepository.create_order(
        order
    )

    assert created_order is not None

    item = OrderItem(
        order_id=created_order.order_id,
        product_id=product.product_id,
        quantity=1,
        price=500.00
    )

    created_item = (
        OrderRepository.create_order_item(item)
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

    ProductRepository.delete(
        product.product_id
    )

    UserRepository.delete(
        user.user_id
    )