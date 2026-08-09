"""
Tests for CheckoutService.
"""

from unittest.mock import patch

import pytest

from models.order import Order
from models.payment import Payment

from services.checkout_service import CheckoutService


# ============================================================
# Validation Tests
# ============================================================


def test_validate_user_id():
    """Test valid user ID."""

    CheckoutService.validate_user_id(1)


def test_validate_user_id_invalid():
    """Test invalid user ID."""

    with pytest.raises(ValueError):
        CheckoutService.validate_user_id(0)


def test_validate_shipping_address():
    """Test valid shipping address."""

    CheckoutService.validate_shipping_address(
        "Pune, Maharashtra"
    )


def test_validate_shipping_address_empty():
    """Test empty shipping address."""

    with pytest.raises(ValueError):
        CheckoutService.validate_shipping_address("")


def test_validate_payment_method():
    """Test valid payment method."""

    CheckoutService.validate_payment_method("upi")


def test_validate_payment_method_invalid():
    """Test invalid payment method."""

    with pytest.raises(ValueError):
        CheckoutService.validate_payment_method(
            "bitcoin"
        )


# ============================================================
# Transaction ID Tests
# ============================================================


def test_generate_transaction_id():
    """Test transaction ID generation."""

    transaction_id = (
        CheckoutService.generate_transaction_id()
    )

    assert transaction_id.startswith("TXN-")
    assert len(transaction_id) == 16


def test_generate_transaction_id_unique():
    """Test transaction IDs are unique."""

    transaction_id_1 = (
        CheckoutService.generate_transaction_id()
    )

    transaction_id_2 = (
        CheckoutService.generate_transaction_id()
    )

    assert transaction_id_1 != transaction_id_2


# ============================================================
# Empty Cart Tests
# ============================================================


def test_checkout_empty_cart():
    """Test checkout cannot proceed with empty cart."""

    with patch(
        "services.checkout_service.CartService.get_cart",
        return_value=[]
    ):
        with pytest.raises(ValueError):
            CheckoutService.checkout(
                user_id=1,
                shipping_address="Pune, Maharashtra",
                payment_method="upi"
            )


# ============================================================
# Successful Checkout Tests
# ============================================================


def test_checkout_success():
    """
    Test complete successful checkout workflow.

    Verifies:
        - Order creation
        - Payment creation
        - Payment success
        - Stock reduction
        - Order confirmation
        - Cart clearing
    """

    cart_item = type(
        "CartItem",
        (),
        {
            "product_id": 1,
            "quantity": 2
        }
    )()

    product = type(
        "Product",
        (),
        {
            "product_id": 1,
            "name": "Laptop",
            "price": 500.00,
            "stock": 10
        }
    )()

    created_order = Order(
        order_id=100,
        user_id=1,
        status="pending",
        shipping_address="Pune, Maharashtra",
        total_amount=1000.00
    )

    created_payment = Payment(
        payment_id=200,
        order_id=100,
        amount=1000.00,
        payment_method="upi",
        transaction_id="TXN-123456789ABC",
        status="pending"
    )

    with patch(
        "services.checkout_service.CartService.get_cart",
        return_value=[cart_item]
    ), patch(
        "services.checkout_service.ProductRepository.get_by_id",
        return_value=product
    ), patch(
        "services.checkout_service.OrderService.create_order",
        return_value=created_order
    ) as mock_create_order, patch(
        "services.checkout_service.PaymentService.create_payment",
        return_value=created_payment
    ) as mock_create_payment, patch(
        "services.checkout_service.PaymentService.update_payment_status",
        return_value=True
    ) as mock_update_payment_status, patch(
        "services.checkout_service.ProductRepository.decrease_stock",
        return_value=True
    ) as mock_decrease_stock, patch(
        "services.checkout_service.OrderService.update_order",
        return_value=True
    ) as mock_update_order, patch(
        "services.checkout_service.CartService.clear_cart",
        return_value=True
    ) as mock_clear_cart:

        result = CheckoutService.checkout(
            user_id=1,
            shipping_address="Pune, Maharashtra",
            payment_method="upi"
        )

    assert result is not None

    assert "order" in result
    assert "payment" in result

    assert result["order"].order_id == 100
    assert result["order"].user_id == 1
    assert result["order"].status == "confirmed"

    assert result["payment"].payment_id == 200
    assert result["payment"].order_id == 100
    assert result["payment"].amount == 1000.00
    assert result["payment"].payment_method == "upi"
    assert result["payment"].status == "successful"

    mock_create_order.assert_called_once()
    mock_create_payment.assert_called_once()

    mock_update_payment_status.assert_called_once_with(
        200,
        "successful"
    )

    mock_decrease_stock.assert_called_once_with(
        1,
        2
    )

    mock_update_order.assert_called_once()
    mock_clear_cart.assert_called_once_with(1)


# ============================================================
# Product Validation Tests
# ============================================================


def test_checkout_invalid_product():
    """Test checkout fails when product does not exist."""

    cart_item = type(
        "CartItem",
        (),
        {
            "product_id": 999,
            "quantity": 1
        }
    )()

    with patch(
        "services.checkout_service.CartService.get_cart",
        return_value=[cart_item]
    ), patch(
        "services.checkout_service.ProductRepository.get_by_id",
        return_value=None
    ):

        with pytest.raises(ValueError):
            CheckoutService.checkout(
                user_id=1,
                shipping_address="Pune, Maharashtra",
                payment_method="upi"
            )


def test_checkout_invalid_cart_product_id():
    """Test checkout fails for invalid product ID."""

    cart_item = type(
        "CartItem",
        (),
        {
            "product_id": None,
            "quantity": 1
        }
    )()

    with patch(
        "services.checkout_service.CartService.get_cart",
        return_value=[cart_item]
    ):

        with pytest.raises(ValueError):
            CheckoutService.checkout(
                user_id=1,
                shipping_address="Pune, Maharashtra",
                payment_method="upi"
            )


def test_checkout_insufficient_stock():
    """Test checkout fails when stock is insufficient."""

    cart_item = type(
        "CartItem",
        (),
        {
            "product_id": 1,
            "quantity": 10
        }
    )()

    product = type(
        "Product",
        (),
        {
            "product_id": 1,
            "name": "Laptop",
            "price": 500.00,
            "stock": 5
        }
    )()

    with patch(
        "services.checkout_service.CartService.get_cart",
        return_value=[cart_item]
    ), patch(
        "services.checkout_service.ProductRepository.get_by_id",
        return_value=product
    ):

        with pytest.raises(ValueError):
            CheckoutService.checkout(
                user_id=1,
                shipping_address="Pune, Maharashtra",
                payment_method="upi"
            )


# ============================================================
# Order Creation Failure Tests
# ============================================================


def test_checkout_order_creation_failure():
    """Test checkout when order creation fails."""

    cart_item = type(
        "CartItem",
        (),
        {
            "product_id": 1,
            "quantity": 1
        }
    )()

    product = type(
        "Product",
        (),
        {
            "product_id": 1,
            "name": "Laptop",
            "price": 500.00,
            "stock": 10
        }
    )()

    with patch(
        "services.checkout_service.CartService.get_cart",
        return_value=[cart_item]
    ), patch(
        "services.checkout_service.ProductRepository.get_by_id",
        return_value=product
    ), patch(
        "services.checkout_service.OrderService.create_order",
        return_value=None
    ):

        result = CheckoutService.checkout(
            user_id=1,
            shipping_address="Pune, Maharashtra",
            payment_method="upi"
        )

    assert result is None


# ============================================================
# Payment Creation Failure Tests
# ============================================================


def test_checkout_payment_creation_failure():
    """
    Test checkout rolls back the order when payment
    creation fails.
    """

    cart_item = type(
        "CartItem",
        (),
        {
            "product_id": 1,
            "quantity": 1
        }
    )()

    product = type(
        "Product",
        (),
        {
            "product_id": 1,
            "name": "Laptop",
            "price": 500.00,
            "stock": 10
        }
    )()

    created_order = Order(
        order_id=100,
        user_id=1,
        status="pending",
        shipping_address="Pune, Maharashtra",
        total_amount=500.00
    )

    with patch(
        "services.checkout_service.CartService.get_cart",
        return_value=[cart_item]
    ), patch(
        "services.checkout_service.ProductRepository.get_by_id",
        return_value=product
    ), patch(
        "services.checkout_service.OrderService.create_order",
        return_value=created_order
    ), patch(
        "services.checkout_service.PaymentService.create_payment",
        return_value=None
    ), patch(
        "services.checkout_service.OrderService.delete_order",
        return_value=True
    ) as mock_delete_order:

        with pytest.raises(RuntimeError):
            CheckoutService.checkout(
                user_id=1,
                shipping_address="Pune, Maharashtra",
                payment_method="upi"
            )

    mock_delete_order.assert_called_once_with(100)


# ============================================================
# Payment Failure Tests
# ============================================================


def test_checkout_payment_failure():
    """
    Test checkout handles payment status update failure.
    """

    cart_item = type(
        "CartItem",
        (),
        {
            "product_id": 1,
            "quantity": 1
        }
    )()

    product = type(
        "Product",
        (),
        {
            "product_id": 1,
            "name": "Laptop",
            "price": 500.00,
            "stock": 10
        }
    )()

    created_order = Order(
        order_id=100,
        user_id=1,
        status="pending",
        shipping_address="Pune, Maharashtra",
        total_amount=500.00
    )

    created_payment = Payment(
        payment_id=200,
        order_id=100,
        amount=500.00,
        payment_method="upi",
        transaction_id="TXN-123456789ABC",
        status="pending"
    )

    with patch(
        "services.checkout_service.CartService.get_cart",
        return_value=[cart_item]
    ), patch(
        "services.checkout_service.ProductRepository.get_by_id",
        return_value=product
    ), patch(
        "services.checkout_service.OrderService.create_order",
        return_value=created_order
    ), patch(
        "services.checkout_service.PaymentService.create_payment",
        return_value=created_payment
    ), patch(
        "services.checkout_service.PaymentService.update_payment_status",
        return_value=False
    ), patch(
        "services.checkout_service.OrderService.delete_order",
        return_value=True
    ) as mock_delete_order, patch(
        "services.checkout_service.PaymentService.delete_payment",
        return_value=True
    ) as mock_delete_payment:

        with pytest.raises(RuntimeError):
            CheckoutService.checkout(
                user_id=1,
                shipping_address="Pune, Maharashtra",
                payment_method="upi"
            )

    mock_delete_order.assert_called_once_with(100)
    mock_delete_payment.assert_called_once_with(200)


# ============================================================
# Stock Update Failure Tests
# ============================================================


def test_checkout_stock_update_failure():
    """
    Test checkout raises an error if stock cannot
    be decreased after successful payment.
    """

    cart_item = type(
        "CartItem",
        (),
        {
            "product_id": 1,
            "quantity": 1
        }
    )()

    product = type(
        "Product",
        (),
        {
            "product_id": 1,
            "name": "Laptop",
            "price": 500.00,
            "stock": 10
        }
    )()

    created_order = Order(
        order_id=100,
        user_id=1,
        status="pending",
        shipping_address="Pune, Maharashtra",
        total_amount=500.00
    )

    created_payment = Payment(
        payment_id=200,
        order_id=100,
        amount=500.00,
        payment_method="upi",
        transaction_id="TXN-123456789ABC",
        status="pending"
    )

    with patch(
        "services.checkout_service.CartService.get_cart",
        return_value=[cart_item]
    ), patch(
        "services.checkout_service.ProductRepository.get_by_id",
        return_value=product
    ), patch(
        "services.checkout_service.OrderService.create_order",
        return_value=created_order
    ), patch(
        "services.checkout_service.PaymentService.create_payment",
        return_value=created_payment
    ), patch(
        "services.checkout_service.PaymentService.update_payment_status",
        return_value=True
    ), patch(
        "services.checkout_service.ProductRepository.decrease_stock",
        return_value=False
    ):

        with pytest.raises(RuntimeError):
            CheckoutService.checkout(
                user_id=1,
                shipping_address="Pune, Maharashtra",
                payment_method="upi"
            )


# ============================================================
# Order Confirmation Failure Tests
# ============================================================


def test_checkout_order_confirmation_failure():
    """
    Test checkout raises an error when the order cannot
    be confirmed after successful payment and stock update.
    """

    cart_item = type(
        "CartItem",
        (),
        {
            "product_id": 1,
            "quantity": 1
        }
    )()

    product = type(
        "Product",
        (),
        {
            "product_id": 1,
            "name": "Laptop",
            "price": 500.00,
            "stock": 10
        }
    )()

    created_order = Order(
        order_id=100,
        user_id=1,
        status="pending",
        shipping_address="Pune, Maharashtra",
        total_amount=500.00
    )

    created_payment = Payment(
        payment_id=200,
        order_id=100,
        amount=500.00,
        payment_method="upi",
        transaction_id="TXN-123456789ABC",
        status="pending"
    )

    with patch(
        "services.checkout_service.CartService.get_cart",
        return_value=[cart_item]
    ), patch(
        "services.checkout_service.ProductRepository.get_by_id",
        return_value=product
    ), patch(
        "services.checkout_service.OrderService.create_order",
        return_value=created_order
    ), patch(
        "services.checkout_service.PaymentService.create_payment",
        return_value=created_payment
    ), patch(
        "services.checkout_service.PaymentService.update_payment_status",
        return_value=True
    ), patch(
        "services.checkout_service.ProductRepository.decrease_stock",
        return_value=True
    ), patch(
        "services.checkout_service.OrderService.update_order",
        return_value=False
    ):

        with pytest.raises(RuntimeError):
            CheckoutService.checkout(
                user_id=1,
                shipping_address="Pune, Maharashtra",
                payment_method="upi"
            )


# ============================================================
# Cart Clearing Failure Tests
# ============================================================


def test_checkout_cart_clear_failure():
    """
    Test checkout raises an error when cart clearing fails
    after the order has already been completed.
    """

    cart_item = type(
        "CartItem",
        (),
        {
            "product_id": 1,
            "quantity": 1
        }
    )()

    product = type(
        "Product",
        (),
        {
            "product_id": 1,
            "name": "Laptop",
            "price": 500.00,
            "stock": 10
        }
    )()

    created_order = Order(
        order_id=100,
        user_id=1,
        status="pending",
        shipping_address="Pune, Maharashtra",
        total_amount=500.00
    )

    created_payment = Payment(
        payment_id=200,
        order_id=100,
        amount=500.00,
        payment_method="upi",
        transaction_id="TXN-123456789ABC",
        status="pending"
    )

    with patch(
        "services.checkout_service.CartService.get_cart",
        return_value=[cart_item]
    ), patch(
        "services.checkout_service.ProductRepository.get_by_id",
        return_value=product
    ), patch(
        "services.checkout_service.OrderService.create_order",
        return_value=created_order
    ), patch(
        "services.checkout_service.PaymentService.create_payment",
        return_value=created_payment
    ), patch(
        "services.checkout_service.PaymentService.update_payment_status",
        return_value=True
    ), patch(
        "services.checkout_service.ProductRepository.decrease_stock",
        return_value=True
    ), patch(
        "services.checkout_service.OrderService.update_order",
        return_value=True
    ), patch(
        "services.checkout_service.CartService.clear_cart",
        return_value=False
    ):

        with pytest.raises(RuntimeError):
            CheckoutService.checkout(
                user_id=1,
                shipping_address="Pune, Maharashtra",
                payment_method="upi"
            )


# ============================================================
# Payment Status Handling Tests
# ============================================================


def test_checkout_payment_status_becomes_successful():
    """
    Test that a pending payment becomes successful
    during checkout.
    """

    cart_item = type(
        "CartItem",
        (),
        {
            "product_id": 1,
            "quantity": 1
        }
    )()

    product = type(
        "Product",
        (),
        {
            "product_id": 1,
            "name": "Laptop",
            "price": 500.00,
            "stock": 10
        }
    )()

    created_order = Order(
        order_id=100,
        user_id=1,
        status="pending",
        shipping_address="Pune, Maharashtra",
        total_amount=500.00
    )

    created_payment = Payment(
        payment_id=200,
        order_id=100,
        amount=500.00,
        payment_method="upi",
        transaction_id="TXN-123456789ABC",
        status="pending"
    )

    with patch(
        "services.checkout_service.CartService.get_cart",
        return_value=[cart_item]
    ), patch(
        "services.checkout_service.ProductRepository.get_by_id",
        return_value=product
    ), patch(
        "services.checkout_service.OrderService.create_order",
        return_value=created_order
    ), patch(
        "services.checkout_service.PaymentService.create_payment",
        return_value=created_payment
    ), patch(
        "services.checkout_service.PaymentService.update_payment_status",
        return_value=True
    ) as mock_update_payment_status, patch(
        "services.checkout_service.ProductRepository.decrease_stock",
        return_value=True
    ), patch(
        "services.checkout_service.OrderService.update_order",
        return_value=True
    ), patch(
        "services.checkout_service.CartService.clear_cart",
        return_value=True
    ):

        result = CheckoutService.checkout(
            user_id=1,
            shipping_address="Pune, Maharashtra",
            payment_method="upi"
        )

    assert result["payment"].status == "successful"

    mock_update_payment_status.assert_called_once_with(
        200,
        "successful"
    )


def test_checkout_does_not_continue_after_payment_failure():
    """
    Test that stock, order confirmation, and cart clearing
    do not happen when payment fails.
    """

    cart_item = type(
        "CartItem",
        (),
        {
            "product_id": 1,
            "quantity": 1
        }
    )()

    product = type(
        "Product",
        (),
        {
            "product_id": 1,
            "name": "Laptop",
            "price": 500.00,
            "stock": 10
        }
    )()

    created_order = Order(
        order_id=100,
        user_id=1,
        status="pending",
        shipping_address="Pune, Maharashtra",
        total_amount=500.00
    )

    created_payment = Payment(
        payment_id=200,
        order_id=100,
        amount=500.00,
        payment_method="upi",
        transaction_id="TXN-123456789ABC",
        status="pending"
    )

    with patch(
        "services.checkout_service.CartService.get_cart",
        return_value=[cart_item]
    ), patch(
        "services.checkout_service.ProductRepository.get_by_id",
        return_value=product
    ), patch(
        "services.checkout_service.OrderService.create_order",
        return_value=created_order
    ), patch(
        "services.checkout_service.PaymentService.create_payment",
        return_value=created_payment
    ), patch(
        "services.checkout_service.PaymentService.update_payment_status",
        return_value=False
    ), patch(
        "services.checkout_service.OrderService.delete_order",
        return_value=True
    ), patch(
        "services.checkout_service.PaymentService.delete_payment",
        return_value=True
    ), patch(
        "services.checkout_service.ProductRepository.decrease_stock",
        return_value=True
    ) as mock_decrease_stock, patch(
        "services.checkout_service.OrderService.update_order",
        return_value=True
    ) as mock_update_order, patch(
        "services.checkout_service.CartService.clear_cart",
        return_value=True
    ) as mock_clear_cart:

        with pytest.raises(RuntimeError):
            CheckoutService.checkout(
                user_id=1,
                shipping_address="Pune, Maharashtra",
                payment_method="upi"
            )

    mock_decrease_stock.assert_not_called()
    mock_update_order.assert_not_called()
    mock_clear_cart.assert_not_called()


def test_checkout_payment_amount_matches_order_total():
    """
    Test that payment amount is created using the
    order's total amount.
    """

    cart_item = type(
        "CartItem",
        (),
        {
            "product_id": 1,
            "quantity": 2
        }
    )()

    product = type(
        "Product",
        (),
        {
            "product_id": 1,
            "name": "Laptop",
            "price": 750.00,
            "stock": 10
        }
    )()

    created_order = Order(
        order_id=100,
        user_id=1,
        status="pending",
        shipping_address="Pune, Maharashtra",
        total_amount=1500.00
    )

    created_payment = Payment(
        payment_id=200,
        order_id=100,
        amount=1500.00,
        payment_method="upi",
        transaction_id="TXN-123456789ABC",
        status="pending"
    )

    with patch(
        "services.checkout_service.CartService.get_cart",
        return_value=[cart_item]
    ), patch(
        "services.checkout_service.ProductRepository.get_by_id",
        return_value=product
    ), patch(
        "services.checkout_service.OrderService.create_order",
        return_value=created_order
    ), patch(
        "services.checkout_service.PaymentService.create_payment",
        return_value=created_payment
    ) as mock_create_payment, patch(
        "services.checkout_service.PaymentService.update_payment_status",
        return_value=True
    ), patch(
        "services.checkout_service.ProductRepository.decrease_stock",
        return_value=True
    ), patch(
        "services.checkout_service.OrderService.update_order",
        return_value=True
    ), patch(
        "services.checkout_service.CartService.clear_cart",
        return_value=True
    ):

        CheckoutService.checkout(
            user_id=1,
            shipping_address="Pune, Maharashtra",
            payment_method="upi"
        )

    payment_argument = (
        mock_create_payment.call_args[0][0]
    )

    assert payment_argument.amount == 1500.00
    assert payment_argument.order_id == 100
    assert payment_argument.status == "pending"
    

# ============================================================
# Order Confirmation Tests
# ============================================================


def test_checkout_confirms_order_after_successful_payment():
    """
    Test that the order is confirmed after successful
    payment and stock update.
    """

    cart_item = type(
        "CartItem",
        (),
        {
            "product_id": 1,
            "quantity": 1
        }
    )()

    product = type(
        "Product",
        (),
        {
            "product_id": 1,
            "name": "Laptop",
            "price": 500.00,
            "stock": 10
        }
    )()

    created_order = Order(
        order_id=100,
        user_id=1,
        status="pending",
        shipping_address="Pune, Maharashtra",
        total_amount=500.00
    )

    created_payment = Payment(
        payment_id=200,
        order_id=100,
        amount=500.00,
        payment_method="upi",
        transaction_id="TXN-123456789ABC",
        status="pending"
    )

    with patch(
        "services.checkout_service.CartService.get_cart",
        return_value=[cart_item]
    ), patch(
        "services.checkout_service.ProductRepository.get_by_id",
        return_value=product
    ), patch(
        "services.checkout_service.OrderService.create_order",
        return_value=created_order
    ), patch(
        "services.checkout_service.PaymentService.create_payment",
        return_value=created_payment
    ), patch(
        "services.checkout_service.PaymentService.update_payment_status",
        return_value=True
    ), patch(
        "services.checkout_service.ProductRepository.decrease_stock",
        return_value=True
    ), patch(
        "services.checkout_service.OrderService.update_order",
        return_value=True
    ) as mock_update_order, patch(
        "services.checkout_service.CartService.clear_cart",
        return_value=True
    ):

        result = CheckoutService.checkout(
            user_id=1,
            shipping_address="Pune, Maharashtra",
            payment_method="upi"
        )

    assert result["order"].status == "confirmed"

    mock_update_order.assert_called_once()

    updated_order = (
        mock_update_order.call_args[0][0]
    )

    assert updated_order.order_id == 100
    assert updated_order.user_id == 1
    assert updated_order.total_amount == 500.00
    assert updated_order.status == "confirmed"


def test_checkout_order_confirmation_preserves_total():
    """
    Test that confirming the order does not change
    the order total.
    """

    cart_item = type(
        "CartItem",
        (),
        {
            "product_id": 1,
            "quantity": 2
        }
    )()

    product = type(
        "Product",
        (),
        {
            "product_id": 1,
            "name": "Keyboard",
            "price": 750.00,
            "stock": 10
        }
    )()

    created_order = Order(
        order_id=101,
        user_id=5,
        status="pending",
        shipping_address="Pune, Maharashtra",
        total_amount=1500.00
    )

    created_payment = Payment(
        payment_id=201,
        order_id=101,
        amount=1500.00,
        payment_method="card",
        transaction_id="TXN-987654321ABC",
        status="pending"
    )

    with patch(
        "services.checkout_service.CartService.get_cart",
        return_value=[cart_item]
    ), patch(
        "services.checkout_service.ProductRepository.get_by_id",
        return_value=product
    ), patch(
        "services.checkout_service.OrderService.create_order",
        return_value=created_order
    ), patch(
        "services.checkout_service.PaymentService.create_payment",
        return_value=created_payment
    ), patch(
        "services.checkout_service.PaymentService.update_payment_status",
        return_value=True
    ), patch(
        "services.checkout_service.ProductRepository.decrease_stock",
        return_value=True
    ), patch(
        "services.checkout_service.OrderService.update_order",
        return_value=True
    ) as mock_update_order, patch(
        "services.checkout_service.CartService.clear_cart",
        return_value=True
    ):

        result = CheckoutService.checkout(
            user_id=5,
            shipping_address="Pune, Maharashtra",
            payment_method="card"
        )

    assert result["order"].status == "confirmed"
    assert result["order"].total_amount == 1500.00
    assert result["order"].user_id == 5

    updated_order = (
        mock_update_order.call_args[0][0]
    )

    assert updated_order.total_amount == 1500.00
    assert updated_order.user_id == 5
    assert updated_order.status == "confirmed"


def test_checkout_does_not_confirm_order_when_payment_fails():
    """
    Test that an order is not confirmed when payment
    processing fails.
    """

    cart_item = type(
        "CartItem",
        (),
        {
            "product_id": 1,
            "quantity": 1
        }
    )()

    product = type(
        "Product",
        (),
        {
            "product_id": 1,
            "name": "Mouse",
            "price": 300.00,
            "stock": 10
        }
    )()

    created_order = Order(
        order_id=102,
        user_id=2,
        status="pending",
        shipping_address="Pune, Maharashtra",
        total_amount=300.00
    )

    created_payment = Payment(
        payment_id=202,
        order_id=102,
        amount=300.00,
        payment_method="upi",
        transaction_id="TXN-111222333ABC",
        status="pending"
    )

    with patch(
        "services.checkout_service.CartService.get_cart",
        return_value=[cart_item]
    ), patch(
        "services.checkout_service.ProductRepository.get_by_id",
        return_value=product
    ), patch(
        "services.checkout_service.OrderService.create_order",
        return_value=created_order
    ), patch(
        "services.checkout_service.PaymentService.create_payment",
        return_value=created_payment
    ), patch(
        "services.checkout_service.PaymentService.update_payment_status",
        return_value=False
    ), patch(
        "services.checkout_service.OrderService.delete_order",
        return_value=True
    ), patch(
        "services.checkout_service.PaymentService.delete_payment",
        return_value=True
    ), patch(
        "services.checkout_service.OrderService.update_order",
        return_value=True
    ) as mock_update_order:

        with pytest.raises(RuntimeError):
            CheckoutService.checkout(
                user_id=2,
                shipping_address="Pune, Maharashtra",
                payment_method="upi"
            )

    mock_update_order.assert_not_called()

    assert created_order.status == "pending"


def test_checkout_order_confirmation_failure():
    """
    Test that checkout fails when the confirmed order
    cannot be persisted.
    """

    cart_item = type(
        "CartItem",
        (),
        {
            "product_id": 1,
            "quantity": 1
        }
    )()

    product = type(
        "Product",
        (),
        {
            "product_id": 1,
            "name": "Monitor",
            "price": 1200.00,
            "stock": 10
        }
    )()

    created_order = Order(
        order_id=103,
        user_id=3,
        status="pending",
        shipping_address="Pune, Maharashtra",
        total_amount=1200.00
    )

    created_payment = Payment(
        payment_id=203,
        order_id=103,
        amount=1200.00,
        payment_method="card",
        transaction_id="TXN-444555666ABC",
        status="pending"
    )

    with patch(
        "services.checkout_service.CartService.get_cart",
        return_value=[cart_item]
    ), patch(
        "services.checkout_service.ProductRepository.get_by_id",
        return_value=product
    ), patch(
        "services.checkout_service.OrderService.create_order",
        return_value=created_order
    ), patch(
        "services.checkout_service.PaymentService.create_payment",
        return_value=created_payment
    ), patch(
        "services.checkout_service.PaymentService.update_payment_status",
        return_value=True
    ), patch(
        "services.checkout_service.ProductRepository.decrease_stock",
        return_value=True
    ), patch(
        "services.checkout_service.OrderService.update_order",
        return_value=False
    ) as mock_update_order, patch(
        "services.checkout_service.CartService.clear_cart",
        return_value=True
    ) as mock_clear_cart:

        with pytest.raises(RuntimeError):
            CheckoutService.checkout(
                user_id=3,
                shipping_address="Pune, Maharashtra",
                payment_method="card"
            )

    mock_update_order.assert_called_once()

    updated_order = (
        mock_update_order.call_args[0][0]
    )

    assert updated_order.status == "confirmed"

    mock_clear_cart.assert_not_called()
    

# ============================================================
# Cart Clearing After Payment Tests
# ============================================================


def test_checkout_clears_cart_after_successful_order():
    """
    Test that the customer's cart is cleared only after
    successful payment, stock update, and order confirmation.
    """

    cart_item = type(
        "CartItem",
        (),
        {
            "product_id": 1,
            "quantity": 1
        }
    )()

    product = type(
        "Product",
        (),
        {
            "product_id": 1,
            "name": "Laptop",
            "price": 500.00,
            "stock": 10
        }
    )()

    created_order = Order(
        order_id=100,
        user_id=7,
        status="pending",
        shipping_address="Pune, Maharashtra",
        total_amount=500.00
    )

    created_payment = Payment(
        payment_id=200,
        order_id=100,
        amount=500.00,
        payment_method="upi",
        transaction_id="TXN-123456789ABC",
        status="pending"
    )

    with patch(
        "services.checkout_service.CartService.get_cart",
        return_value=[cart_item]
    ), patch(
        "services.checkout_service.ProductRepository.get_by_id",
        return_value=product
    ), patch(
        "services.checkout_service.OrderService.create_order",
        return_value=created_order
    ), patch(
        "services.checkout_service.PaymentService.create_payment",
        return_value=created_payment
    ), patch(
        "services.checkout_service.PaymentService.update_payment_status",
        return_value=True
    ), patch(
        "services.checkout_service.ProductRepository.decrease_stock",
        return_value=True
    ), patch(
        "services.checkout_service.OrderService.update_order",
        return_value=True
    ), patch(
        "services.checkout_service.CartService.clear_cart",
        return_value=True
    ) as mock_clear_cart:

        result = CheckoutService.checkout(
            user_id=7,
            shipping_address="Pune, Maharashtra",
            payment_method="upi"
        )

    assert result is not None

    mock_clear_cart.assert_called_once_with(7)


def test_checkout_does_not_clear_cart_when_payment_fails():
    """
    Test that the cart remains untouched when payment fails.
    """

    cart_item = type(
        "CartItem",
        (),
        {
            "product_id": 1,
            "quantity": 1
        }
    )()

    product = type(
        "Product",
        (),
        {
            "product_id": 1,
            "name": "Laptop",
            "price": 500.00,
            "stock": 10
        }
    )()

    created_order = Order(
        order_id=100,
        user_id=8,
        status="pending",
        shipping_address="Pune, Maharashtra",
        total_amount=500.00
    )

    created_payment = Payment(
        payment_id=200,
        order_id=100,
        amount=500.00,
        payment_method="upi",
        transaction_id="TXN-123456789ABC",
        status="pending"
    )

    with patch(
        "services.checkout_service.CartService.get_cart",
        return_value=[cart_item]
    ), patch(
        "services.checkout_service.ProductRepository.get_by_id",
        return_value=product
    ), patch(
        "services.checkout_service.OrderService.create_order",
        return_value=created_order
    ), patch(
        "services.checkout_service.PaymentService.create_payment",
        return_value=created_payment
    ), patch(
        "services.checkout_service.PaymentService.update_payment_status",
        return_value=False
    ), patch(
        "services.checkout_service.OrderService.delete_order",
        return_value=True
    ), patch(
        "services.checkout_service.PaymentService.delete_payment",
        return_value=True
    ), patch(
        "services.checkout_service.CartService.clear_cart",
        return_value=True
    ) as mock_clear_cart:

        with pytest.raises(RuntimeError):
            CheckoutService.checkout(
                user_id=8,
                shipping_address="Pune, Maharashtra",
                payment_method="upi"
            )

    mock_clear_cart.assert_not_called()


def test_checkout_does_not_clear_cart_when_stock_update_fails():
    """
    Test that the cart is not cleared when stock update fails.
    """

    cart_item = type(
        "CartItem",
        (),
        {
            "product_id": 1,
            "quantity": 1
        }
    )()

    product = type(
        "Product",
        (),
        {
            "product_id": 1,
            "name": "Keyboard",
            "price": 750.00,
            "stock": 10
        }
    )()

    created_order = Order(
        order_id=101,
        user_id=9,
        status="pending",
        shipping_address="Pune, Maharashtra",
        total_amount=750.00
    )

    created_payment = Payment(
        payment_id=201,
        order_id=101,
        amount=750.00,
        payment_method="card",
        transaction_id="TXN-987654321ABC",
        status="pending"
    )

    with patch(
        "services.checkout_service.CartService.get_cart",
        return_value=[cart_item]
    ), patch(
        "services.checkout_service.ProductRepository.get_by_id",
        return_value=product
    ), patch(
        "services.checkout_service.OrderService.create_order",
        return_value=created_order
    ), patch(
        "services.checkout_service.PaymentService.create_payment",
        return_value=created_payment
    ), patch(
        "services.checkout_service.PaymentService.update_payment_status",
        return_value=True
    ), patch(
        "services.checkout_service.ProductRepository.decrease_stock",
        return_value=False
    ), patch(
        "services.checkout_service.CartService.clear_cart",
        return_value=True
    ) as mock_clear_cart:

        with pytest.raises(RuntimeError):
            CheckoutService.checkout(
                user_id=9,
                shipping_address="Pune, Maharashtra",
                payment_method="card"
            )

    mock_clear_cart.assert_not_called()


def test_checkout_does_not_clear_cart_when_order_confirmation_fails():
    """
    Test that the cart is not cleared when order confirmation fails.
    """

    cart_item = type(
        "CartItem",
        (),
        {
            "product_id": 1,
            "quantity": 1
        }
    )()

    product = type(
        "Product",
        (),
        {
            "product_id": 1,
            "name": "Monitor",
            "price": 1200.00,
            "stock": 10
        }
    )()

    created_order = Order(
        order_id=102,
        user_id=10,
        status="pending",
        shipping_address="Pune, Maharashtra",
        total_amount=1200.00
    )

    created_payment = Payment(
        payment_id=202,
        order_id=102,
        amount=1200.00,
        payment_method="upi",
        transaction_id="TXN-111222333ABC",
        status="pending"
    )

    with patch(
        "services.checkout_service.CartService.get_cart",
        return_value=[cart_item]
    ), patch(
        "services.checkout_service.ProductRepository.get_by_id",
        return_value=product
    ), patch(
        "services.checkout_service.OrderService.create_order",
        return_value=created_order
    ), patch(
        "services.checkout_service.PaymentService.create_payment",
        return_value=created_payment
    ), patch(
        "services.checkout_service.PaymentService.update_payment_status",
        return_value=True
    ), patch(
        "services.checkout_service.ProductRepository.decrease_stock",
        return_value=True
    ), patch(
        "services.checkout_service.OrderService.update_order",
        return_value=False
    ), patch(
        "services.checkout_service.CartService.clear_cart",
        return_value=True
    ) as mock_clear_cart:

        with pytest.raises(RuntimeError):
            CheckoutService.checkout(
                user_id=10,
                shipping_address="Pune, Maharashtra",
                payment_method="upi"
            )

    mock_clear_cart.assert_not_called()


def test_checkout_cart_clear_failure_is_reported():
    """
    Test that checkout reports an error if the cart cannot
    be cleared after the order is completed.
    """

    cart_item = type(
        "CartItem",
        (),
        {
            "product_id": 1,
            "quantity": 1
        }
    )()

    product = type(
        "Product",
        (),
        {
            "product_id": 1,
            "name": "Mouse",
            "price": 300.00,
            "stock": 10
        }
    )()

    created_order = Order(
        order_id=103,
        user_id=11,
        status="pending",
        shipping_address="Pune, Maharashtra",
        total_amount=300.00
    )

    created_payment = Payment(
        payment_id=203,
        order_id=103,
        amount=300.00,
        payment_method="upi",
        transaction_id="TXN-444555666ABC",
        status="pending"
    )

    with patch(
        "services.checkout_service.CartService.get_cart",
        return_value=[cart_item]
    ), patch(
        "services.checkout_service.ProductRepository.get_by_id",
        return_value=product
    ), patch(
        "services.checkout_service.OrderService.create_order",
        return_value=created_order
    ), patch(
        "services.checkout_service.PaymentService.create_payment",
        return_value=created_payment
    ), patch(
        "services.checkout_service.PaymentService.update_payment_status",
        return_value=True
    ), patch(
        "services.checkout_service.ProductRepository.decrease_stock",
        return_value=True
    ), patch(
        "services.checkout_service.OrderService.update_order",
        return_value=True
    ), patch(
        "services.checkout_service.CartService.clear_cart",
        return_value=False
    ) as mock_clear_cart:

        with pytest.raises(RuntimeError):
            CheckoutService.checkout(
                user_id=11,
                shipping_address="Pune, Maharashtra",
                payment_method="upi"
            )

    mock_clear_cart.assert_called_once_with(11)