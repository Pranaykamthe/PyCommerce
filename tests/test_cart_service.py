"""
test_cart_service.py
--------------------
Tests for CartService validation and business logic.
"""

import pytest

from models.cart import Cart
from services.cart_service import CartService


def test_validate_user_id():
    """Test valid user ID."""

    CartService.validate_user_id(1)


def test_invalid_user_id():
    """Test invalid user ID."""

    with pytest.raises(ValueError):
        CartService.validate_user_id(0)


def test_validate_product_id():
    """Test valid product ID."""

    CartService.validate_product_id(1)


def test_invalid_product_id():
    """Test invalid product ID."""

    with pytest.raises(ValueError):
        CartService.validate_product_id(0)


def test_validate_quantity():
    """Test valid quantity."""

    CartService.validate_quantity(1)
    CartService.validate_quantity(10)


def test_invalid_quantity():
    """Test invalid quantity."""

    with pytest.raises(ValueError):
        CartService.validate_quantity(0)


def test_negative_quantity():
    """Test negative quantity."""

    with pytest.raises(ValueError):
        CartService.validate_quantity(-1)


def test_cart_model():
    """Test creating a Cart object."""

    cart = Cart(
        cart_id=1,
        user_id=2,
        product_id=3,
        quantity=5
    )

    assert cart.cart_id == 1
    assert cart.user_id == 2
    assert cart.product_id == 3
    assert cart.quantity == 5


def test_get_cart_invalid_user():
    """Test getting cart with invalid user."""

    with pytest.raises(ValueError):
        CartService.get_cart(0)


def test_get_cart_item_invalid_id():
    """Test getting cart item with invalid ID."""

    with pytest.raises(ValueError):
        CartService.get_cart_item(0)


def test_get_product_from_cart_invalid_user():
    """Test invalid user ID."""

    with pytest.raises(ValueError):
        CartService.get_product_from_cart(
            0,
            1
        )


def test_get_product_from_cart_invalid_product():
    """Test invalid product ID."""

    with pytest.raises(ValueError):
        CartService.get_product_from_cart(
            1,
            0
        )


def test_add_to_cart_invalid_user():
    """Test adding with invalid user."""

    with pytest.raises(ValueError):
        CartService.add_to_cart(
            user_id=0,
            product_id=1,
            quantity=1
        )


def test_add_to_cart_invalid_product():
    """Test adding with invalid product."""

    with pytest.raises(ValueError):
        CartService.add_to_cart(
            user_id=1,
            product_id=0,
            quantity=1
        )


def test_add_to_cart_invalid_quantity():
    """Test adding with invalid quantity."""

    with pytest.raises(ValueError):
        CartService.add_to_cart(
            user_id=1,
            product_id=1,
            quantity=0
        )


def test_update_invalid_quantity():
    """Test updating with invalid quantity."""

    with pytest.raises(ValueError):
        CartService.update_quantity(
            user_id=1,
            product_id=1,
            quantity=0
        )


def test_remove_invalid_user():
    """Test removing with invalid user."""

    with pytest.raises(ValueError):
        CartService.remove_from_cart(
            user_id=0,
            product_id=1
        )


def test_remove_invalid_product():
    """Test removing with invalid product."""

    with pytest.raises(ValueError):
        CartService.remove_from_cart(
            user_id=1,
            product_id=0
        )


def test_clear_invalid_user():
    """Test clearing with invalid user."""

    with pytest.raises(ValueError):
        CartService.clear_cart(0)