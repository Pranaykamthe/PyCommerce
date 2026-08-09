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


# ============================================================
# Create Payment Tests
# ============================================================


def test_create_payment(monkeypatch):
    """Test creating a valid payment."""

    payment = Payment(
        order_id=1,
        amount=500.00,
        payment_method="upi",
        status="pending",
        transaction_id="TXN-123456"
    )

    def mock_create(payment):
        payment.payment_id = 1
        return payment

    monkeypatch.setattr(
        "services.payment_service.PaymentRepository.create",
        mock_create
    )

    result = PaymentService.create_payment(payment)

    assert result is not None
    assert result.payment_id == 1
    assert result.order_id == 1
    assert result.amount == 500.00
    assert result.payment_method == "upi"
    assert result.status == "pending"
    assert result.transaction_id == "TXN-123456"


def test_create_payment_invalid_order_id():
    """Test creating payment with invalid order ID."""

    payment = Payment(
        order_id=0,
        amount=500.00,
        payment_method="upi",
        status="pending"
    )

    with pytest.raises(ValueError):
        PaymentService.create_payment(payment)


def test_create_payment_invalid_method():
    """Test creating payment with invalid payment method."""

    payment = Payment(
        order_id=1,
        amount=500.00,
        payment_method="bitcoin",
        status="pending"
    )

    with pytest.raises(ValueError):
        PaymentService.create_payment(payment)


def test_create_payment_invalid_status():
    """Test creating payment with invalid status."""

    payment = Payment(
        order_id=1,
        amount=500.00,
        payment_method="upi",
        status="completed"
    )

    with pytest.raises(ValueError):
        PaymentService.create_payment(payment)


def test_create_payment_invalid_amount():
    """Test creating payment with invalid amount."""

    payment = Payment(
        order_id=1,
        amount=0,
        payment_method="upi",
        status="pending"
    )

    with pytest.raises(ValueError):
        PaymentService.create_payment(payment)


def test_create_payment_method_normalization(monkeypatch):
    """Test payment method is normalized before creation."""

    payment = Payment(
        order_id=1,
        amount=500.00,
        payment_method=" UPI ",
        status="pending"
    )

    def mock_create(payment):
        payment.payment_id = 1
        return payment

    monkeypatch.setattr(
        "services.payment_service.PaymentRepository.create",
        mock_create
    )

    result = PaymentService.create_payment(payment)

    assert result is not None
    assert result.payment_method == "upi"


def test_create_payment_status_normalization(monkeypatch):
    """Test payment status is normalized before creation."""

    payment = Payment(
        order_id=1,
        amount=500.00,
        payment_method="upi",
        status=" PENDING "
    )

    def mock_create(payment):
        payment.payment_id = 1
        return payment

    monkeypatch.setattr(
        "services.payment_service.PaymentRepository.create",
        mock_create
    )

    result = PaymentService.create_payment(payment)

    assert result is not None
    assert result.status == "pending"


def test_create_payment_transaction_id_normalization(monkeypatch):
    """Test transaction ID is stripped before creation."""

    payment = Payment(
        order_id=1,
        amount=500.00,
        payment_method="upi",
        status="pending",
        transaction_id="  TXN-123456  "
    )

    def mock_create(payment):
        payment.payment_id = 1
        return payment

    monkeypatch.setattr(
        "services.payment_service.PaymentRepository.create",
        mock_create
    )

    result = PaymentService.create_payment(payment)

    assert result is not None
    assert result.transaction_id == "TXN-123456"


# ============================================================
# Get Payment Tests
# ============================================================


def test_get_payment(monkeypatch):
    """Test getting a payment by ID."""

    payment = Payment(
        payment_id=1,
        order_id=10,
        amount=500.00,
        payment_method="upi",
        status="successful"
    )

    def mock_get_by_id(payment_id):
        return payment

    monkeypatch.setattr(
        "services.payment_service.PaymentRepository.get_by_id",
        mock_get_by_id
    )

    result = PaymentService.get_payment(1)

    assert result is not None
    assert result.payment_id == 1
    assert result.order_id == 10
    assert result.status == "successful"


def test_get_payment_invalid_id():
    """Test getting payment with invalid ID."""

    with pytest.raises(ValueError):
        PaymentService.get_payment(0)


def test_get_payment_by_order(monkeypatch):
    """Test getting payment by order ID."""

    payment = Payment(
        payment_id=1,
        order_id=10,
        amount=500.00,
        payment_method="upi",
        status="successful"
    )

    def mock_get_by_order_id(order_id):
        return payment

    monkeypatch.setattr(
        "services.payment_service.PaymentRepository.get_by_order_id",
        mock_get_by_order_id
    )

    result = PaymentService.get_payment_by_order(10)

    assert result is not None
    assert result.payment_id == 1
    assert result.order_id == 10


def test_get_payment_by_order_invalid_id():
    """Test getting payment by invalid order ID."""

    with pytest.raises(ValueError):
        PaymentService.get_payment_by_order(0)


def test_get_all_payments(monkeypatch):
    """Test getting all payments."""

    payments = [
        Payment(
            payment_id=1,
            order_id=10,
            amount=500.00,
            payment_method="upi",
            status="successful"
        ),
        Payment(
            payment_id=2,
            order_id=11,
            amount=750.00,
            payment_method="card",
            status="pending"
        )
    ]

    def mock_get_all():
        return payments

    monkeypatch.setattr(
        "services.payment_service.PaymentRepository.get_all",
        mock_get_all
    )

    result = PaymentService.get_all_payments()

    assert len(result) == 2
    assert result[0].payment_id == 1
    assert result[1].payment_id == 2


# ============================================================
# Update Payment Tests
# ============================================================


def test_update_payment(monkeypatch):
    """Test updating a payment."""

    payment = Payment(
        payment_id=1,
        order_id=10,
        amount=600.00,
        payment_method="card",
        status="successful",
        transaction_id="TXN-999999"
    )

    def mock_update(payment):
        return True

    monkeypatch.setattr(
        "services.payment_service.PaymentRepository.update",
        mock_update
    )

    result = PaymentService.update_payment(payment)

    assert result is True
    assert payment.payment_method == "card"
    assert payment.status == "successful"


def test_update_payment_without_id():
    """Test updating payment without payment ID."""

    payment = Payment(
        order_id=10,
        amount=500.00,
        payment_method="upi",
        status="pending"
    )

    with pytest.raises(ValueError):
        PaymentService.update_payment(payment)


def test_update_payment_without_order_id():
    """Test updating payment without order ID."""

    payment = Payment(
        payment_id=1,
        amount=500.00,
        payment_method="upi",
        status="pending"
    )

    with pytest.raises(ValueError):
        PaymentService.update_payment(payment)


def test_update_payment_invalid_method():
    """Test updating payment with invalid method."""

    payment = Payment(
        payment_id=1,
        order_id=10,
        amount=500.00,
        payment_method="bitcoin",
        status="pending"
    )

    with pytest.raises(ValueError):
        PaymentService.update_payment(payment)


def test_update_payment_invalid_status():
    """Test updating payment with invalid status."""

    payment = Payment(
        payment_id=1,
        order_id=10,
        amount=500.00,
        payment_method="upi",
        status="completed"
    )

    with pytest.raises(ValueError):
        PaymentService.update_payment(payment)


def test_update_payment_invalid_amount():
    """Test updating payment with invalid amount."""

    payment = Payment(
        payment_id=1,
        order_id=10,
        amount=0,
        payment_method="upi",
        status="pending"
    )

    with pytest.raises(ValueError):
        PaymentService.update_payment(payment)


# ============================================================
# Update Payment Status Tests
# ============================================================


def test_update_payment_status(monkeypatch):
    """Test updating payment status."""

    payment = Payment(
        payment_id=1,
        order_id=10,
        amount=500.00,
        payment_method="upi",
        status="pending"
    )

    def mock_get_by_id(payment_id):
        return payment

    def mock_update(payment):
        return True

    monkeypatch.setattr(
        "services.payment_service.PaymentRepository.get_by_id",
        mock_get_by_id
    )

    monkeypatch.setattr(
        "services.payment_service.PaymentRepository.update",
        mock_update
    )

    result = PaymentService.update_payment_status(
        1,
        "successful"
    )

    assert result is True
    assert payment.status == "successful"


def test_update_payment_status_normalization(monkeypatch):
    """Test payment status is normalized before update."""

    payment = Payment(
        payment_id=1,
        order_id=10,
        amount=500.00,
        payment_method="upi",
        status="pending"
    )

    def mock_get_by_id(payment_id):
        return payment

    def mock_update(payment):
        return True

    monkeypatch.setattr(
        "services.payment_service.PaymentRepository.get_by_id",
        mock_get_by_id
    )

    monkeypatch.setattr(
        "services.payment_service.PaymentRepository.update",
        mock_update
    )

    result = PaymentService.update_payment_status(
        1,
        " SUCCESSFUL "
    )

    assert result is True
    assert payment.status == "successful"


def test_update_payment_status_invalid_payment_id():
    """Test status update with invalid payment ID."""

    with pytest.raises(ValueError):
        PaymentService.update_payment_status(
            0,
            "successful"
        )


def test_update_payment_status_invalid_status():
    """Test status update with invalid status."""

    with pytest.raises(ValueError):
        PaymentService.update_payment_status(
            1,
            "completed"
        )


def test_update_payment_status_payment_not_found(monkeypatch):
    """Test status update when payment does not exist."""

    def mock_get_by_id(payment_id):
        return None

    monkeypatch.setattr(
        "services.payment_service.PaymentRepository.get_by_id",
        mock_get_by_id
    )

    with pytest.raises(ValueError):
        PaymentService.update_payment_status(
            1,
            "successful"
        )


# ============================================================
# Delete Payment Tests
# ============================================================


def test_delete_payment(monkeypatch):
    """Test deleting a payment."""

    def mock_delete(payment_id):
        return True

    monkeypatch.setattr(
        "services.payment_service.PaymentRepository.delete",
        mock_delete
    )

    result = PaymentService.delete_payment(1)

    assert result is True


def test_delete_payment_invalid_id():
    """Test deleting payment with invalid ID."""

    with pytest.raises(ValueError):
        PaymentService.delete_payment(0)


# ============================================================
# Payment Status Transition Tests
# ============================================================


def test_valid_pending_to_successful_transition():
    """Test pending payment can become successful."""

    PaymentService.validate_status_transition(
        "pending",
        "successful"
    )


def test_valid_pending_to_failed_transition():
    """Test pending payment can become failed."""

    PaymentService.validate_status_transition(
        "pending",
        "failed"
    )


def test_valid_successful_to_refunded_transition():
    """Test successful payment can become refunded."""

    PaymentService.validate_status_transition(
        "successful",
        "refunded"
    )


def test_valid_failed_to_pending_transition():
    """Test failed payment can return to pending."""

    PaymentService.validate_status_transition(
        "failed",
        "pending"
    )


def test_invalid_successful_to_pending_transition():
    """Test successful payment cannot become pending."""

    with pytest.raises(ValueError):
        PaymentService.validate_status_transition(
            "successful",
            "pending"
        )


def test_invalid_successful_to_failed_transition():
    """Test successful payment cannot become failed."""

    with pytest.raises(ValueError):
        PaymentService.validate_status_transition(
            "successful",
            "failed"
        )


def test_invalid_failed_to_successful_transition():
    """Test failed payment cannot become successful directly."""

    with pytest.raises(ValueError):
        PaymentService.validate_status_transition(
            "failed",
            "successful"
        )


def test_invalid_refunded_to_successful_transition():
    """Test refunded payment cannot become successful."""

    with pytest.raises(ValueError):
        PaymentService.validate_status_transition(
            "refunded",
            "successful"
        )


def test_invalid_refunded_to_pending_transition():
    """Test refunded payment cannot become pending."""

    with pytest.raises(ValueError):
        PaymentService.validate_status_transition(
            "refunded",
            "pending"
        )


def test_status_transition_normalization():
    """Test status transition accepts uppercase and spaces."""

    PaymentService.validate_status_transition(
        " PENDING ",
        " SUCCESSFUL "
    )


def test_invalid_current_payment_status():
    """Test invalid current status is rejected."""

    with pytest.raises(ValueError):
        PaymentService.validate_status_transition(
            "unknown",
            "successful"
        )


def test_invalid_new_payment_status():
    """Test invalid new status is rejected."""

    with pytest.raises(ValueError):
        PaymentService.validate_status_transition(
            "pending",
            "completed"
        )