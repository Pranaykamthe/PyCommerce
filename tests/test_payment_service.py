"""
Tests for PaymentService.
"""

import pytest

from models.payment import Payment
from services.payment_service import PaymentService


# ============================================================
# Validation Tests
# ============================================================

def test_valid_order_id():
    """Test valid order ID."""

    PaymentService.validate_order_id(1)


def test_invalid_order_id():
    """Test invalid order ID."""

    with pytest.raises(ValueError):
        PaymentService.validate_order_id(0)


def test_negative_order_id():
    """Test negative order ID."""

    with pytest.raises(ValueError):
        PaymentService.validate_order_id(-1)


def test_valid_payment_id():
    """Test valid payment ID."""

    PaymentService.validate_payment_id(1)


def test_invalid_payment_id():
    """Test invalid payment ID."""

    with pytest.raises(ValueError):
        PaymentService.validate_payment_id(0)


def test_valid_payment_method():
    """Test valid payment methods."""

    PaymentService.validate_payment_method("cash")
    PaymentService.validate_payment_method("card")
    PaymentService.validate_payment_method("upi")
    PaymentService.validate_payment_method("net_banking")


def test_invalid_payment_method():
    """Test invalid payment method."""

    with pytest.raises(ValueError):
        PaymentService.validate_payment_method("bitcoin")


def test_empty_payment_method():
    """Test empty payment method."""

    with pytest.raises(ValueError):
        PaymentService.validate_payment_method("")


def test_valid_payment_status():
    """Test valid payment statuses."""

    PaymentService.validate_payment_status("pending")
    PaymentService.validate_payment_status("successful")
    PaymentService.validate_payment_status("failed")
    PaymentService.validate_payment_status("refunded")


def test_invalid_payment_status():
    """Test invalid payment status."""

    with pytest.raises(ValueError):
        PaymentService.validate_payment_status("completed")


def test_empty_payment_status():
    """Test empty payment status."""

    with pytest.raises(ValueError):
        PaymentService.validate_payment_status("")


def test_valid_amount():
    """Test valid payment amount."""

    PaymentService.validate_amount(100.00)


def test_zero_amount():
    """Test zero payment amount."""

    with pytest.raises(ValueError):
        PaymentService.validate_amount(0)


def test_negative_amount():
    """Test negative payment amount."""

    with pytest.raises(ValueError):
        PaymentService.validate_amount(-100)


# ============================================================
# Model Test
# ============================================================

def test_payment_model():
    """Test Payment model with service."""

    payment = Payment(
        order_id=1,
        payment_method="upi",
        amount=500.00,
        status="pending"
    )

    assert payment.order_id == 1
    assert payment.payment_method == "upi"
    assert payment.amount == 500.00
    assert payment.status == "pending"