"""
Business logic related to payments.
"""

from typing import Optional

from models.payment import Payment
from repositories.payment_repository import PaymentRepository


class PaymentService:
    """Provides business operations for payments."""

    ALLOWED_METHODS = {
        "cash",
        "card",
        "upi",
        "net_banking"
    }

    ALLOWED_STATUSES = {
        "pending",
        "successful",
        "failed",
        "refunded"
    }

    # ========================================================
    # Validation
    # ========================================================

    @staticmethod
    def validate_order_id(
        order_id: int
    ) -> None:
        """Validate an order ID."""

        if order_id <= 0:
            raise ValueError(
                "Order ID must be greater than zero."
            )

    @staticmethod
    def validate_payment_id(
        payment_id: int
    ) -> None:
        """Validate a payment ID."""

        if payment_id <= 0:
            raise ValueError(
                "Payment ID must be greater than zero."
            )

    @staticmethod
    def validate_payment_method(
        payment_method: str
    ) -> None:
        """Validate payment method."""

        if not payment_method:
            raise ValueError(
                "Payment method cannot be empty."
            )

        if payment_method not in PaymentService.ALLOWED_METHODS:
            raise ValueError(
                "Invalid payment method."
            )

    @staticmethod
    def validate_payment_status(
        payment_status: str
    ) -> None:
        """Validate payment status."""

        if not payment_status:
            raise ValueError(
                "Payment status cannot be empty."
            )

        if payment_status not in PaymentService.ALLOWED_STATUSES:
            raise ValueError(
                "Invalid payment status."
            )

    @staticmethod
    def validate_status(
        status: str
    ) -> None:
        """
        Validate payment status.

        This method is kept for compatibility with
        existing service methods.
        """

        PaymentService.validate_payment_status(
            status
        )

    @staticmethod
    def validate_amount(
        amount: float
    ) -> None:
        """Validate payment amount."""

        if amount <= 0:
            raise ValueError(
                "Payment amount must be greater than zero."
            )

    # ========================================================
    # Create Payment
    # ========================================================

    @staticmethod
    def create_payment(
        payment: Payment
    ) -> Optional[Payment]:
        """
        Validate and create a payment.
        """

        if payment.order_id is None:
            raise ValueError(
                "Order ID is required."
            )

        PaymentService.validate_order_id(
            payment.order_id
        )

        PaymentService.validate_payment_method(
            payment.payment_method
        )

        PaymentService.validate_payment_status(
            payment.status
        )

        PaymentService.validate_amount(
            payment.amount
        )

        payment.payment_method = (
            payment.payment_method.strip().lower()
        )

        payment.status = (
            payment.status.strip().lower()
        )

        if payment.transaction_id is not None:
            payment.transaction_id = (
                payment.transaction_id.strip()
            )

        return PaymentRepository.create(
            payment
        )

    # ========================================================
    # Get Payment
    # ========================================================

    @staticmethod
    def get_payment(
        payment_id: int
    ) -> Optional[Payment]:
        """Get payment by payment ID."""

        PaymentService.validate_payment_id(
            payment_id
        )

        return PaymentRepository.get_by_id(
            payment_id
        )

    @staticmethod
    def get_payment_by_order(
        order_id: int
    ) -> Optional[Payment]:
        """Get payment associated with an order."""

        PaymentService.validate_order_id(
            order_id
        )

        return PaymentRepository.get_by_order_id(
            order_id
        )

    @staticmethod
    def get_all_payments() -> list[Payment]:
        """Get all payments."""

        return PaymentRepository.get_all()

    # ========================================================
    # Update Payment
    # ========================================================

    @staticmethod
    def update_payment(
        payment: Payment
    ) -> bool:
        """
        Validate and update an existing payment.
        """

        if payment.payment_id is None:
            raise ValueError(
                "Payment ID is required."
            )

        if payment.order_id is None:
            raise ValueError(
                "Order ID is required."
            )

        PaymentService.validate_payment_id(
            payment.payment_id
        )

        PaymentService.validate_order_id(
            payment.order_id
        )

        PaymentService.validate_payment_method(
            payment.payment_method
        )

        PaymentService.validate_payment_status(
            payment.status
        )

        PaymentService.validate_amount(
            payment.amount
        )

        payment.payment_method = (
            payment.payment_method.strip().lower()
        )

        payment.status = (
            payment.status.strip().lower()
        )

        if payment.transaction_id is not None:
            payment.transaction_id = (
                payment.transaction_id.strip()
            )

        return PaymentRepository.update(
            payment
        )

    # ========================================================
    # Update Payment Status
    # ========================================================

    @staticmethod
    def update_payment_status(
        payment_id: int,
        status: str
    ) -> bool:
        """
        Update the status of a payment.
        """

        PaymentService.validate_payment_id(
            payment_id
        )

        PaymentService.validate_payment_status(
            status
        )

        payment = PaymentRepository.get_by_id(
            payment_id
        )

        if payment is None:
            raise ValueError(
                "Payment not found."
            )

        payment.status = (
            status.strip().lower()
        )

        return PaymentRepository.update(
            payment
        )

    # ========================================================
    # Delete Payment
    # ========================================================

    @staticmethod
    def delete_payment(
        payment_id: int
    ) -> bool:
        """Delete a payment."""

        PaymentService.validate_payment_id(
            payment_id
        )

        return PaymentRepository.delete(
            payment_id
        )