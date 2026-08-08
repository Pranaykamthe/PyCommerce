"""
test_model_validation.py
------------------------
Validation and consistency tests for PyCommerce models.
"""

from models import (
    User,
    Category,
    Product,
    Cart,
    Order,
    OrderItem,
    Payment,
    Review,
)


def test_user_role():
    """Test that a user can represent a customer."""

    user = User(
        user_id=1,
        name="Test Customer",
        email="customer@example.com",
        role="customer",
    )

    assert user.role == "customer"


def test_category_data():
    """Test category data consistency."""

    category = Category(
        category_id=1,
        name="Electronics",
        description="Electronic products",
    )

    assert category.category_id == 1
    assert category.name == "Electronics"


def test_product_category_relationship():
    """Test that a product references a category."""

    product = Product(
        product_id=101,
        category_id=1,
        name="Wireless Mouse",
        price=799.00,
        stock=25,
    )

    assert product.category_id == 1
    assert product.price > 0
    assert product.stock >= 0


def test_cart_relationship():
    """Test that a cart item references a user and product."""

    cart = Cart(
        cart_id=1,
        user_id=10,
        product_id=101,
        quantity=2,
    )

    assert cart.user_id == 10
    assert cart.product_id == 101
    assert cart.quantity > 0


def test_order_relationship():
    """Test that an order references a user."""

    order = Order(
        order_id=5001,
        user_id=10,
        total_amount=1598.00,
        status="pending",
    )

    assert order.user_id == 10
    assert order.total_amount > 0
    assert order.status == "pending"


def test_order_item_relationship():
    """Test that an order item references an order and product."""

    item = OrderItem(
        order_item_id=1,
        order_id=5001,
        product_id=101,
        quantity=2,
        price=799.00,
    )

    assert item.order_id == 5001
    assert item.product_id == 101
    assert item.quantity > 0
    assert item.price > 0


def test_payment_relationship():
    """Test that a payment references an order."""

    payment = Payment(
        payment_id=1,
        order_id=5001,
        amount=1598.00,
        payment_method="UPI",
        transaction_id="TXN123456",
        status="completed",
    )

    assert payment.order_id == 5001
    assert payment.amount > 0
    assert payment.payment_method == "UPI"
    assert payment.transaction_id != ""
    assert payment.status == "completed"


def test_review_relationship():
    """Test that a review references a user and product."""

    review = Review(
        review_id=1,
        user_id=10,
        product_id=101,
        rating=5,
        comment="Excellent product!",
    )

    assert review.user_id == 10
    assert review.product_id == 101
    assert 1 <= review.rating <= 5
    assert review.comment != ""