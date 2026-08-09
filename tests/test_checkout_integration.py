"""
Real database integration tests for the PyCommerce checkout flow.
"""

from uuid import uuid4

from models.user import User
from models.product import Product
from models.cart import Cart

from repositories.user_repository import UserRepository
from repositories.product_repository import ProductRepository
from repositories.cart_repository import CartRepository
from repositories.order_repository import OrderRepository
from repositories.payment_repository import PaymentRepository

from services.checkout_service import CheckoutService


# ============================================================
# Test Data Helpers
# ============================================================


def create_test_user():
    """Create a unique customer for integration testing."""

    unique_id = uuid4().hex[:8]

    user = User(
        name="Checkout Integration Test",
        email=f"checkout_{unique_id}@pycommerce.test",
        password="pass12345",
        phone=f"88888{unique_id[:5]}",
        address="Pune",
        role="customer"
    )

    created = UserRepository.create(user)

    assert created is not None
    assert created.user_id is not None

    return created


def get_existing_category_id():
    """
    Get an existing category ID from the database.

    The current project does not contain a
    CategoryRepository, so the integration test uses
    an existing category instead of creating one.
    """

    from config.database import (
        get_connection,
        close_connection
    )

    connection = get_connection()

    assert connection is not None

    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            SELECT category_id
            FROM categories
            ORDER BY category_id
            LIMIT 1
            """
        )

        row = cursor.fetchone()

        assert row is not None, (
            "No category exists in the database. "
            "Create at least one category before "
            "running checkout integration tests."
        )

        return row[0]

    finally:
        cursor.close()
        close_connection(connection)


def create_test_product(category_id):
    """Create a unique product for integration testing."""

    unique_id = uuid4().hex[:8]

    product = Product(
        name=f"Integration Product {unique_id}",
        description="Integration test product",
        price=999.00,
        stock=10,
        category_id=category_id
    )

    created = ProductRepository.create(product)

    assert created is not None
    assert created.product_id is not None

    return created


# ============================================================
# Full Checkout Integration
# ============================================================


def test_full_checkout_integration():
    """
    Test the complete checkout workflow against MySQL.

    Flow:

        User
          ↓
        Product
          ↓
        Cart
          ↓
        Checkout
          ↓
        Order
          ↓
        Payment
          ↓
        Stock reduction
          ↓
        Order confirmation
          ↓
        Cart clearing
    """

    user = create_test_user()

    category_id = get_existing_category_id()

    product = create_test_product(
        category_id
    )

    cart = Cart(
        user_id=user.user_id,
        product_id=product.product_id,
        quantity=2
    )

    created_cart = CartRepository.create(
        cart
    )

    assert created_cart is not None

    original_stock = product.stock

    result = CheckoutService.checkout(
        user_id=user.user_id,
        shipping_address="Pune, Maharashtra",
        payment_method="upi"
    )

    assert result is not None

    order = result["order"]
    payment = result["payment"]

    # --------------------------------------------------------
    # Verify Order
    # --------------------------------------------------------

    assert order is not None
    assert order.order_id is not None
    assert order.user_id == user.user_id
    assert order.status == "confirmed"

    assert order.total_amount == (
        product.price * 2
    )

    # --------------------------------------------------------
    # Verify Payment
    # --------------------------------------------------------

    assert payment is not None
    assert payment.payment_id is not None
    assert payment.order_id == order.order_id
    assert payment.amount == order.total_amount
    assert payment.payment_method == "upi"
    assert payment.status == "successful"
    assert payment.transaction_id.startswith("TXN-")

    # --------------------------------------------------------
    # Verify Payment in Database
    # --------------------------------------------------------

    stored_payment = PaymentRepository.get_by_id(
        payment.payment_id
    )

    assert stored_payment is not None
    assert stored_payment.order_id == order.order_id
    assert stored_payment.status == "successful"
    assert stored_payment.amount == order.total_amount

    # --------------------------------------------------------
    # Verify Order in Database
    # --------------------------------------------------------

    stored_order = OrderRepository.get_order_by_id(
        order.order_id
    )

    assert stored_order is not None
    assert stored_order.user_id == user.user_id
    assert stored_order.status == "confirmed"
    assert stored_order.total_amount == order.total_amount

    # --------------------------------------------------------
    # Verify Stock Reduction
    # --------------------------------------------------------

    stored_product = ProductRepository.get_by_id(
        product.product_id
    )

    assert stored_product is not None

    assert stored_product.stock == (
        original_stock - 2
    )

    # --------------------------------------------------------
    # Verify Cart Was Cleared
    # --------------------------------------------------------

    remaining_cart = CartRepository.get_by_user(
        user.user_id
    )

    assert remaining_cart == []


# ============================================================
# Verify Order History After Checkout
# ============================================================


def test_checkout_order_appears_in_customer_history():
    """
    Test that a completed checkout appears in the
    customer's order history.
    """

    user = create_test_user()

    category_id = get_existing_category_id()

    product = create_test_product(
        category_id
    )

    cart = Cart(
        user_id=user.user_id,
        product_id=product.product_id,
        quantity=1
    )

    created_cart = CartRepository.create(
        cart
    )

    assert created_cart is not None

    result = CheckoutService.checkout(
        user_id=user.user_id,
        shipping_address="Pune, Maharashtra",
        payment_method="card"
    )

    assert result is not None

    order = result["order"]

    orders = OrderRepository.get_orders_by_user(
        user.user_id
    )

    order_ids = [
        item.order_id
        for item in orders
    ]

    assert order.order_id in order_ids


# ============================================================
# Verify Order Items After Checkout
# ============================================================


def test_checkout_creates_order_items():
    """
    Test that checkout creates the corresponding
    order items in the database.
    """

    user = create_test_user()

    category_id = get_existing_category_id()

    product = create_test_product(
        category_id
    )

    cart = Cart(
        user_id=user.user_id,
        product_id=product.product_id,
        quantity=3
    )

    created_cart = CartRepository.create(
        cart
    )

    assert created_cart is not None

    result = CheckoutService.checkout(
        user_id=user.user_id,
        shipping_address="Pune, Maharashtra",
        payment_method="cash"
    )

    assert result is not None

    order = result["order"]

    items = OrderRepository.get_order_items(
        order.order_id
    )

    assert isinstance(items, list)
    assert len(items) == 1

    item = items[0]

    assert item.order_id == order.order_id
    assert item.product_id == product.product_id
    assert item.quantity == 3
    assert item.price == product.price