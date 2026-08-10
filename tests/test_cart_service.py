"""
test_cart_service.py
--------------------
Tests for CartService validation and business logic.
"""

import pytest
from unittest.mock import patch

from models.cart import Cart
from models.product import Product
from services.cart_service import CartService


# ============================================================
# Validation Tests
# ============================================================

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


def test_validate_cart_id():
    """Test valid cart ID."""

    CartService.validate_cart_id(1)


def test_invalid_cart_id():
    """Test invalid cart ID."""

    with pytest.raises(ValueError):
        CartService.validate_cart_id(0)


# ============================================================
# Cart Model Test
# ============================================================

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


# ============================================================
# Get Cart Tests
# ============================================================

def test_get_cart_invalid_user():
    """Test getting cart with invalid user."""

    with pytest.raises(ValueError):
        CartService.get_cart(0)


def test_get_cart():
    """Test getting all cart items for a user."""

    cart_items = [
        Cart(
            cart_id=1,
            user_id=1,
            product_id=10,
            quantity=2
        ),
        Cart(
            cart_id=2,
            user_id=1,
            product_id=20,
            quantity=1
        )
    ]

    with patch(
        "services.cart_service.CartRepository.get_by_user",
        return_value=cart_items
    ) as mock_get:

        result = CartService.get_cart(1)

    assert result == cart_items
    mock_get.assert_called_once_with(1)


# ============================================================
# Get Cart Item Tests
# ============================================================

def test_get_cart_item_invalid_id():
    """Test getting cart item with invalid ID."""

    with pytest.raises(ValueError):
        CartService.get_cart_item(0)


def test_get_cart_item():
    """Test getting a cart item by cart ID."""

    cart = Cart(
        cart_id=5,
        user_id=1,
        product_id=10,
        quantity=2
    )

    with patch(
        "services.cart_service.CartRepository.get_by_id",
        return_value=cart
    ) as mock_get:

        result = CartService.get_cart_item(5)

    assert result is cart
    mock_get.assert_called_once_with(5)


def test_get_cart_item_not_found():
    """Test getting a cart item that does not exist."""

    with patch(
        "services.cart_service.CartRepository.get_by_id",
        return_value=None
    ):

        result = CartService.get_cart_item(999)

    assert result is None


# ============================================================
# Get Product From Cart Tests
# ============================================================

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


def test_get_product_from_cart():
    """Test getting a specific product from a user's cart."""

    cart = Cart(
        cart_id=5,
        user_id=1,
        product_id=10,
        quantity=2
    )

    with patch(
        "services.cart_service.CartRepository.get_by_user_and_product",
        return_value=cart
    ) as mock_get:

        result = CartService.get_product_from_cart(
            user_id=1,
            product_id=10
        )

    assert result is cart

    mock_get.assert_called_once_with(
        1,
        10
    )


def test_get_product_from_cart_not_found():
    """Test product not found in user's cart."""

    with patch(
        "services.cart_service.CartRepository.get_by_user_and_product",
        return_value=None
    ):

        result = CartService.get_product_from_cart(
            user_id=1,
            product_id=10
        )

    assert result is None


# ============================================================
# Add To Cart - Validation Tests
# ============================================================

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


# ============================================================
# Add To Cart - Business Logic Tests
# ============================================================

def test_add_to_cart_new_product():
    """Test adding a new product to the cart."""

    product = Product(
        product_id=10,
        category_id=1,
        name="Test Product",
        description="Test product",
        price=500.00,
        stock=10,
        image_url="test.jpg"
    )

    created_cart = Cart(
        cart_id=1,
        user_id=1,
        product_id=10,
        quantity=2
    )

    with patch(
        "services.cart_service.ProductRepository.get_by_id",
        return_value=product
    ), patch(
        "services.cart_service.CartRepository.get_by_user_and_product",
        return_value=None
    ), patch(
        "services.cart_service.CartRepository.create",
        return_value=created_cart
    ) as mock_create:

        result = CartService.add_to_cart(
            user_id=1,
            product_id=10,
            quantity=2
        )

    assert result is True

    created_item = mock_create.call_args[0][0]

    assert created_item.user_id == 1
    assert created_item.product_id == 10
    assert created_item.quantity == 2


def test_add_to_cart_product_not_found():
    """Test adding a product that does not exist."""

    with patch(
        "services.cart_service.ProductRepository.get_by_id",
        return_value=None
    ):

        with pytest.raises(
            ValueError,
            match="Product not found."
        ):
            CartService.add_to_cart(
                user_id=1,
                product_id=10,
                quantity=1
            )


def test_add_to_cart_out_of_stock():
    """Test adding an out-of-stock product."""

    product = Product(
        product_id=10,
        category_id=1,
        name="Out Of Stock Product",
        description="Test product",
        price=500.00,
        stock=0,
        image_url=""
    )

    with patch(
        "services.cart_service.ProductRepository.get_by_id",
        return_value=product
    ):

        with pytest.raises(
            ValueError,
            match="Product is out of stock."
        ):
            CartService.add_to_cart(
                user_id=1,
                product_id=10,
                quantity=1
            )


def test_add_to_cart_existing_product():
    """Test increasing quantity of an existing cart item."""

    product = Product(
        product_id=10,
        category_id=1,
        name="Test Product",
        description="Test product",
        price=500.00,
        stock=10,
        image_url=""
    )

    existing_cart = Cart(
        cart_id=5,
        user_id=1,
        product_id=10,
        quantity=2
    )

    with patch(
        "services.cart_service.ProductRepository.get_by_id",
        return_value=product
    ), patch(
        "services.cart_service.CartRepository.get_by_user_and_product",
        return_value=existing_cart
    ), patch(
        "services.cart_service.CartRepository.update_quantity",
        return_value=True
    ) as mock_update:

        result = CartService.add_to_cart(
            user_id=1,
            product_id=10,
            quantity=3
        )

    assert result is True

    mock_update.assert_called_once_with(
        cart_id=5,
        quantity=5
    )


def test_add_to_cart_insufficient_stock():
    """Test adding more items than available stock."""

    product = Product(
        product_id=10,
        category_id=1,
        name="Limited Product",
        description="Test product",
        price=500.00,
        stock=5,
        image_url=""
    )

    existing_cart = Cart(
        cart_id=5,
        user_id=1,
        product_id=10,
        quantity=4
    )

    with patch(
        "services.cart_service.ProductRepository.get_by_id",
        return_value=product
    ), patch(
        "services.cart_service.CartRepository.get_by_user_and_product",
        return_value=existing_cart
    ):

        with pytest.raises(
            ValueError,
            match="Only 5 item\\(s\\) are available in stock."
        ):
            CartService.add_to_cart(
                user_id=1,
                product_id=10,
                quantity=2
            )


def test_add_to_cart_repository_create_failure():
    """Test when cart creation fails."""

    product = Product(
        product_id=10,
        category_id=1,
        name="Test Product",
        description="Test product",
        price=500.00,
        stock=10,
        image_url=""
    )

    with patch(
        "services.cart_service.ProductRepository.get_by_id",
        return_value=product
    ), patch(
        "services.cart_service.CartRepository.get_by_user_and_product",
        return_value=None
    ), patch(
        "services.cart_service.CartRepository.create",
        return_value=None
    ):

        result = CartService.add_to_cart(
            user_id=1,
            product_id=10,
            quantity=2
        )

    assert result is False


def test_add_to_cart_existing_update_failure():
    """Test when updating an existing cart item fails."""

    product = Product(
        product_id=10,
        category_id=1,
        name="Test Product",
        description="Test product",
        price=500.00,
        stock=10,
        image_url=""
    )

    existing_cart = Cart(
        cart_id=5,
        user_id=1,
        product_id=10,
        quantity=2
    )

    with patch(
        "services.cart_service.ProductRepository.get_by_id",
        return_value=product
    ), patch(
        "services.cart_service.CartRepository.get_by_user_and_product",
        return_value=existing_cart
    ), patch(
        "services.cart_service.CartRepository.update_quantity",
        return_value=False
    ):

        result = CartService.add_to_cart(
            user_id=1,
            product_id=10,
            quantity=3
        )

    assert result is False


# ============================================================
# Update Quantity Tests
# ============================================================

def test_update_invalid_quantity():
    """Test updating with invalid quantity."""

    with pytest.raises(ValueError):
        CartService.update_quantity(
            user_id=1,
            product_id=1,
            quantity=0
        )


def test_update_quantity():
    """Test updating an existing cart item quantity."""

    product = Product(
        product_id=10,
        category_id=1,
        name="Test Product",
        description="Test product",
        price=500.00,
        stock=10,
        image_url=""
    )

    cart = Cart(
        cart_id=5,
        user_id=1,
        product_id=10,
        quantity=2
    )

    with patch(
        "services.cart_service.ProductRepository.get_by_id",
        return_value=product
    ), patch(
        "services.cart_service.CartRepository.get_by_user_and_product",
        return_value=cart
    ), patch(
        "services.cart_service.CartRepository.update_quantity",
        return_value=True
    ) as mock_update:

        result = CartService.update_quantity(
            user_id=1,
            product_id=10,
            quantity=5
        )

    assert result is True

    mock_update.assert_called_once_with(
        cart_id=5,
        quantity=5
    )


def test_update_quantity_product_not_found():
    """Test updating quantity for a missing product."""

    with patch(
        "services.cart_service.ProductRepository.get_by_id",
        return_value=None
    ):

        with pytest.raises(
            ValueError,
            match="Product not found."
        ):
            CartService.update_quantity(
                user_id=1,
                product_id=10,
                quantity=2
            )


def test_update_quantity_exceeds_stock():
    """Test updating quantity above available stock."""

    product = Product(
        product_id=10,
        category_id=1,
        name="Test Product",
        description="Test product",
        price=500.00,
        stock=3,
        image_url=""
    )

    with patch(
        "services.cart_service.ProductRepository.get_by_id",
        return_value=product
    ):

        with pytest.raises(
            ValueError,
            match="Only 3 item\\(s\\) are available in stock."
        ):
            CartService.update_quantity(
                user_id=1,
                product_id=10,
                quantity=5
            )


def test_update_quantity_product_not_in_cart():
    """Test updating a product that is not in the cart."""

    product = Product(
        product_id=10,
        category_id=1,
        name="Test Product",
        description="Test product",
        price=500.00,
        stock=10,
        image_url=""
    )

    with patch(
        "services.cart_service.ProductRepository.get_by_id",
        return_value=product
    ), patch(
        "services.cart_service.CartRepository.get_by_user_and_product",
        return_value=None
    ):

        with pytest.raises(
            ValueError,
            match="Product is not in the cart."
        ):
            CartService.update_quantity(
                user_id=1,
                product_id=10,
                quantity=2
            )


def test_update_quantity_repository_failure():
    """Test when updating cart quantity fails."""

    product = Product(
        product_id=10,
        category_id=1,
        name="Test Product",
        description="Test product",
        price=500.00,
        stock=10,
        image_url=""
    )

    cart = Cart(
        cart_id=5,
        user_id=1,
        product_id=10,
        quantity=2
    )

    with patch(
        "services.cart_service.ProductRepository.get_by_id",
        return_value=product
    ), patch(
        "services.cart_service.CartRepository.get_by_user_and_product",
        return_value=cart
    ), patch(
        "services.cart_service.CartRepository.update_quantity",
        return_value=False
    ):

        result = CartService.update_quantity(
            user_id=1,
            product_id=10,
            quantity=5
        )

    assert result is False


# ============================================================
# Remove From Cart Tests
# ============================================================

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


def test_remove_from_cart():
    """Test removing a product from the cart."""

    cart = Cart(
        cart_id=5,
        user_id=1,
        product_id=10,
        quantity=2
    )

    with patch(
        "services.cart_service.CartRepository.get_by_user_and_product",
        return_value=cart
    ), patch(
        "services.cart_service.CartRepository.delete",
        return_value=True
    ) as mock_delete:

        result = CartService.remove_from_cart(
            user_id=1,
            product_id=10
        )

    assert result is True

    mock_delete.assert_called_once_with(5)


def test_remove_from_cart_product_not_found():
    """Test removing a product that is not in the cart."""

    with patch(
        "services.cart_service.CartRepository.get_by_user_and_product",
        return_value=None
    ):

        with pytest.raises(
            ValueError,
            match="Product is not in the cart."
        ):
            CartService.remove_from_cart(
                user_id=1,
                product_id=10
            )


def test_remove_from_cart_repository_failure():
    """Test when deleting a cart item fails."""

    cart = Cart(
        cart_id=5,
        user_id=1,
        product_id=10,
        quantity=2
    )

    with patch(
        "services.cart_service.CartRepository.get_by_user_and_product",
        return_value=cart
    ), patch(
        "services.cart_service.CartRepository.delete",
        return_value=False
    ):

        result = CartService.remove_from_cart(
            user_id=1,
            product_id=10
        )

    assert result is False


# ============================================================
# Clear Cart Tests
# ============================================================

def test_clear_invalid_user():
    """Test clearing with invalid user."""

    with pytest.raises(ValueError):
        CartService.clear_cart(0)


def test_clear_cart():
    """Test clearing all cart items."""

    with patch(
        "services.cart_service.CartRepository.clear_user_cart",
        return_value=True
    ) as mock_clear:

        result = CartService.clear_cart(1)

    assert result is True

    mock_clear.assert_called_once_with(1)


def test_clear_empty_cart():
    """Test clearing an already empty cart."""

    with patch(
        "services.cart_service.CartRepository.clear_user_cart",
        return_value=False
    ):

        result = CartService.clear_cart(1)

    assert result is False