"""
Business logic for the checkout workflow.
"""

import uuid
from typing import Optional

from models.order import Order
from models.order_item import OrderItem
from models.payment import Payment

from services.cart_service import CartService
from services.order_service import OrderService
from services.payment_service import PaymentService

from repositories.product_repository import ProductRepository


class CheckoutService:
    """Coordinates cart, order, payment, and stock operations."""

    # ========================================================
    # Validation
    # ========================================================

    @staticmethod
    def validate_user_id(
        user_id: int
    ) -> None:
        """Validate customer user ID."""

        if user_id <= 0:
            raise ValueError(
                "User ID must be greater than zero."
            )

    @staticmethod
    def validate_shipping_address(
        shipping_address: str
    ) -> None:
        """Validate shipping address."""

        OrderService.validate_shipping_address(
            shipping_address
        )

    @staticmethod
    def validate_payment_method(
        payment_method: str
    ) -> None:
        """Validate payment method."""

        PaymentService.validate_payment_method(
            payment_method.strip().lower()
        )

    # ========================================================
    # Transaction ID
    # ========================================================

    @staticmethod
    def generate_transaction_id() -> str:
        """Generate a unique transaction ID."""

        return (
            f"TXN-{uuid.uuid4().hex[:12].upper()}"
        )

    # ========================================================
    # Checkout
    # ========================================================

    @staticmethod
    def checkout(
        user_id: int,
        shipping_address: str,
        payment_method: str
    ) -> Optional[dict]:
        """
        Complete the checkout workflow.

        Steps:
            1. Validate customer.
            2. Load cart.
            3. Validate stock.
            4. Create order and order items.
            5. Create payment.
            6. Mark payment successful.
            7. Confirm order.
            8. Decrease product stock.
            9. Clear cart.

        Returns:
            Dictionary containing order and payment,
            or None if order creation fails.
        """

        # ----------------------------------------------------
        # Validate input
        # ----------------------------------------------------

        CheckoutService.validate_user_id(
            user_id
        )

        CheckoutService.validate_shipping_address(
            shipping_address
        )

        CheckoutService.validate_payment_method(
            payment_method
        )

        payment_method = (
            payment_method.strip().lower()
        )

        # ----------------------------------------------------
        # Get cart
        # ----------------------------------------------------

        cart_items = CartService.get_cart(
            user_id
        )

        if not cart_items:

            raise ValueError(
                "Cannot checkout with an empty cart."
            )

        # ----------------------------------------------------
        # Validate products and stock
        # ----------------------------------------------------

        order_items = []

        for cart_item in cart_items:

            if cart_item.product_id is None:

                raise ValueError(
                    "Cart contains an invalid product."
                )

            product = ProductRepository.get_by_id(
                cart_item.product_id
            )

            if product is None:

                raise ValueError(
                    f"Product {cart_item.product_id} "
                    "was not found."
                )

            if product.stock < cart_item.quantity:

                raise ValueError(
                    f"Insufficient stock for "
                    f"'{product.name}'. "
                    f"Available: {product.stock}, "
                    f"requested: {cart_item.quantity}."
                )

            order_items.append(
                OrderItem(
                    product_id=product.product_id,
                    quantity=cart_item.quantity,
                    price=product.price
                )
            )

        # ----------------------------------------------------
        # Create order
        # ----------------------------------------------------

        order = Order(
            user_id=user_id,
            status="pending",
            shipping_address=shipping_address
        )

        created_order = OrderService.create_order(
            order,
            order_items
        )

        if created_order is None:

            return None

        # ----------------------------------------------------
        # Create payment
        # ----------------------------------------------------

        payment = Payment(
            order_id=created_order.order_id,
            amount=created_order.total_amount,
            payment_method=payment_method,
            transaction_id=(
                CheckoutService.generate_transaction_id()
            ),
            status="pending"
        )

        created_payment = PaymentService.create_payment(
            payment
        )

        if created_payment is None:

            OrderService.delete_order(
                created_order.order_id
            )

            raise RuntimeError(
                "Unable to create payment."
            )

        # ----------------------------------------------------
        # Simulate successful payment
        # ----------------------------------------------------

        payment_success = (
            PaymentService.update_payment_status(
                created_payment.payment_id,
                "successful"
            )
        )

        # ----------------------------------------------------
        # IMPORTANT:
        # Update the Python object as well as
        # the database record.
        # ----------------------------------------------------

        if payment_success:

            created_payment.status = (
                "successful"
            )

        # ----------------------------------------------------
        # Handle payment failure
        # ----------------------------------------------------

        if not payment_success:

            OrderService.delete_order(
                created_order.order_id
            )

            PaymentService.delete_payment(
                created_payment.payment_id
            )

            raise RuntimeError(
                "Payment could not be completed."
            )

        # ----------------------------------------------------
        # Decrease product stock
        # ----------------------------------------------------

        for item in order_items:

            stock_updated = (
                ProductRepository.decrease_stock(
                    item.product_id,
                    item.quantity
                )
            )

            if not stock_updated:

                raise RuntimeError(
                    "Unable to update product stock "
                    "after successful payment."
                )

        # ----------------------------------------------------
        # Confirm order
        # ----------------------------------------------------

        created_order.status = "confirmed"

        order_updated = (
            OrderService.update_order(
                created_order
            )
        )

        if not order_updated:

            raise RuntimeError(
                "Payment succeeded, but order "
                "could not be confirmed."
            )

        # ----------------------------------------------------
        # Clear cart
        # ----------------------------------------------------

        cart_cleared = CartService.clear_cart(
            user_id
        )

        if not cart_cleared:

            raise RuntimeError(
                "Order completed, but cart "
                "could not be cleared."
            )

        # ----------------------------------------------------
        # Return checkout result
        # ----------------------------------------------------

        return {
            "order": created_order,
            "payment": created_payment
        }