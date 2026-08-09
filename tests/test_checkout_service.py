from unittest.mock import patch

import pytest

from services.checkout_service import CheckoutService


def test_validate_user_id():
    CheckoutService.validate_user_id(1)


def test_validate_user_id_invalid():
    with pytest.raises(ValueError):
        CheckoutService.validate_user_id(0)


def test_validate_shipping_address():
    CheckoutService.validate_shipping_address(
        "Pune, Maharashtra"
    )


def test_validate_shipping_address_empty():
    with pytest.raises(ValueError):
        CheckoutService.validate_shipping_address("")


def test_validate_payment_method():
    CheckoutService.validate_payment_method("upi")


def test_validate_payment_method_invalid():
    with pytest.raises(ValueError):
        CheckoutService.validate_payment_method(
            "bitcoin"
        )


def test_generate_transaction_id():
    transaction_id = (
        CheckoutService.generate_transaction_id()
    )

    assert transaction_id.startswith("TXN-")
    assert len(transaction_id) == 16


def test_checkout_empty_cart():
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