"""
test_cart_model.py
------------------
Tests for the Cart model.
"""

from models.cart import Cart


def test_create_cart():
    """Test creating a cart item."""

    cart = Cart(
        cart_id=1,
        user_id=10,
        product_id=101,
        quantity=2,
    )

    assert cart.cart_id == 1
    assert cart.user_id == 10
    assert cart.product_id == 101
    assert cart.quantity == 2


def test_cart_default_values():
    """Test cart default values."""

    cart = Cart()

    assert cart.cart_id is None
    assert cart.user_id is None
    assert cart.product_id is None
    assert cart.quantity == 1
    assert cart.added_at is None


def test_cart_string():
    """Test Cart string representation."""

    cart = Cart(
        cart_id=1,
        user_id=10,
        product_id=101,
        quantity=2,
    )

    result = str(cart)

    assert "1" in result
    assert "10" in result
    assert "101" in result
    assert "2" in result