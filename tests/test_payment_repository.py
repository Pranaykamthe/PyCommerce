"""
Tests for PaymentRepository.
"""

from uuid import uuid4

from models.payment import Payment
from models.order import Order
from models.user import User

from repositories.payment_repository import PaymentRepository
from repositories.order_repository import OrderRepository
from repositories.user_repository import UserRepository


# ============================================================
# Test Data Helpers
# ============================================================

def create_test_user() -> User:
    """Create a unique test user."""

    unique_id = uuid4().hex[:8]

    return User(
        name="Payment Test User",
        email=f"payment_test_{unique_id}@pycommerce.test",
        password="pass12345",
        phone=f"99999{unique_id[:5]}",
        address="Pune",
        role="customer"
    )


def create_test_order() -> Order:
    """Create a test order."""

    user = UserRepository.create(
        create_test_user()
    )

    assert user is not None
    assert user.user_id is not None

    order = Order(
        user_id=user.user_id,
        total_amount=500.00,
        status="pending",
        shipping_address="Pune"
    )

    created_order = OrderRepository.create_order(
        order
    )

    assert created_order is not None
    assert created_order.order_id is not None

    return created_order


def create_test_payment() -> Payment:
    """Create a unique test payment."""

    order = create_test_order()

    unique_id = uuid4().hex[:12]

    payment = Payment(
        order_id=order.order_id,
        payment_method="upi",
        transaction_id=f"TEST-TXN-{unique_id}",
        amount=500.00,
        status="pending"
    )

    return payment


# ============================================================
# Create Payment
# ============================================================

def test_create_payment():
    """Test creating a payment."""

    payment = create_test_payment()

    created = PaymentRepository.create(
        payment
    )

    assert created is not None
    assert created.payment_id is not None
    assert created.order_id == payment.order_id
    assert created.payment_method == "upi"
    assert created.status == "pending"
    assert created.amount == 500.00


# ============================================================
# Get Payment By ID
# ============================================================

def test_get_payment_by_id():
    """Test retrieving a payment by ID."""

    payment = create_test_payment()

    created = PaymentRepository.create(
        payment
    )

    assert created is not None
    assert created.payment_id is not None

    found = PaymentRepository.get_by_id(
        created.payment_id
    )

    assert found is not None
    assert found.payment_id == created.payment_id
    assert found.order_id == created.order_id
    assert found.payment_method == "upi"
    assert found.status == "pending"
    assert found.amount == 500.00


# ============================================================
# Get Payment Not Found
# ============================================================

def test_get_payment_not_found():
    """Test retrieving a payment that does not exist."""

    payment = PaymentRepository.get_by_id(
        999999999
    )

    assert payment is None


# ============================================================
# Get Payment By Order
# ============================================================

def test_get_payment_by_order():
    """Test retrieving payment by order ID."""

    payment = create_test_payment()

    created = PaymentRepository.create(
        payment
    )

    assert created is not None
    assert created.order_id is not None

    found = PaymentRepository.get_by_order_id(
        created.order_id
    )

    assert found is not None
    assert found.payment_id == created.payment_id
    assert found.order_id == created.order_id
    assert found.payment_method == "upi"
    assert found.status == "pending"


# ============================================================
# Get Payment By Order Not Found
# ============================================================

def test_get_payment_by_order_not_found():
    """Test payment lookup for an order without payment."""

    payment = PaymentRepository.get_by_order_id(
        999999999
    )

    assert payment is None


# ============================================================
# Get All Payments
# ============================================================

def test_get_all_payments():
    """Test retrieving all payments."""

    payment = create_test_payment()

    created = PaymentRepository.create(
        payment
    )

    assert created is not None

    payments = PaymentRepository.get_all()

    assert isinstance(payments, list)

    payment_ids = [
        item.payment_id
        for item in payments
    ]

    assert created.payment_id in payment_ids


# ============================================================
# Update Payment
# ============================================================

def test_update_payment():
    """Test updating an existing payment."""

    payment = create_test_payment()

    created = PaymentRepository.create(
        payment
    )

    assert created is not None
    assert created.payment_id is not None

    created.payment_method = "card"
    created.status = "successful"
    created.transaction_id = (
        f"TEST-TXN-UPDATED-{uuid4().hex[:8]}"
    )
    created.amount = 750.00

    result = PaymentRepository.update(
        created
    )

    assert result is True

    updated = PaymentRepository.get_by_id(
        created.payment_id
    )

    assert updated is not None
    assert updated.payment_method == "card"
    assert updated.status == "successful"
    assert updated.transaction_id == created.transaction_id
    assert updated.amount == 750.00


# ============================================================
# Update Payment Without ID
# ============================================================

def test_update_payment_without_id():
    """Test updating a payment without payment ID."""

    payment = Payment(
        order_id=1,
        payment_method="upi",
        transaction_id=(
            f"TEST-TXN-NO-ID-{uuid4().hex[:8]}"
        ),
        amount=500.00,
        status="pending"
    )

    result = PaymentRepository.update(
        payment
    )

    assert result is False


# ============================================================
# Delete Payment
# ============================================================

def test_delete_payment():
    """Test deleting a payment."""

    payment = create_test_payment()

    created = PaymentRepository.create(
        payment
    )

    assert created is not None
    assert created.payment_id is not None

    result = PaymentRepository.delete(
        created.payment_id
    )

    assert result is True

    deleted = PaymentRepository.get_by_id(
        created.payment_id
    )

    assert deleted is None


# ============================================================
# Delete Payment Not Found
# ============================================================

def test_delete_payment_not_found():
    """Test deleting a payment that does not exist."""

    result = PaymentRepository.delete(
        999999999
    )

    assert result is False