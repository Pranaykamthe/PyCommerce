"""
test_payment_model.py
---------------------
Tests for the Payment model.
"""

from models.payment import Payment


def test_create_payment():
    """Test creating a payment."""

    payment = Payment(
        payment_id=1,
        order_id=5001,
        amount=1598.00,
        payment_method="card",
        transaction_id="TXN123456",
        status="completed",
    )

    assert payment.payment_id == 1
    assert payment.order_id == 5001
    assert payment.amount == 1598.00
    assert payment.payment_method == "card"
    assert payment.transaction_id == "TXN123456"
    assert payment.status == "completed"


def test_payment_default_values():
    """Test payment default values."""

    payment = Payment()

    assert payment.payment_id is None
    assert payment.order_id is None
    assert payment.amount == 0.0
    assert payment.payment_method == ""
    assert payment.transaction_id == ""
    assert payment.status == "pending"
    assert payment.paid_at is None


def test_payment_string():
    """Test Payment string representation."""

    payment = Payment(
        payment_id=1,
        order_id=5001,
        amount=1598.00,
        payment_method="UPI",
        status="completed",
    )

    result = str(payment)

    assert "1" in result
    assert "5001" in result
    assert "1598.0" in result
    assert "UPI" in result
    assert "completed" in result