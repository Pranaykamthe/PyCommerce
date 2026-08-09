"""
Unit and integration tests for WishlistService.
"""

import uuid

import pytest

from models.product import Product
from models.user import User

from repositories.product_repository import ProductRepository
from repositories.user_repository import UserRepository
from repositories.wishlist_repository import WishlistRepository

from services.auth_service import AuthService
from services.wishlist_service import WishlistService


# ============================================================
# TEST DATA HELPERS
# ============================================================

def create_test_user() -> User:
    """Create a temporary test user."""

    email = (
        f"wishlist_service_{uuid.uuid4().hex[:10]}"
        "@pycommerce.test"
    )

    return User(
        name="Wishlist Service Test",
        email=email,
        password=AuthService.hash_password(
            "TestPassword123"
        ),
        phone="9999999999",
        address="Test Address",
        role="customer"
    )


def create_test_product() -> Product:
    """Create a temporary test product."""

    return Product(
        category_id=1,
        name=(
            f"Wishlist Service Product "
            f"{uuid.uuid4().hex[:8]}"
        ),
        description="Wishlist service test product",
        price=500.00,
        stock=20,
        image_url="wishlist-service-test.jpg"
    )


def create_user_and_product():
    """Create a temporary user and product."""

    user = UserRepository.create(
        create_test_user()
    )

    assert user is not None

    product = ProductRepository.create(
        create_test_product()
    )

    assert product is not None

    return user, product


def cleanup_user_and_product(
    user_id: int,
    product_id: int
):
    """Remove temporary wishlist test data."""

    WishlistService.clear_wishlist(
        user_id
    )

    ProductRepository.delete(
        product_id
    )

    UserRepository.delete(
        user_id
    )


# ============================================================
# VALIDATION
# ============================================================

def test_validate_user_id():
    """Test valid user ID."""

    WishlistService.validate_user_id(1)


def test_invalid_user_id():
    """Test invalid user ID."""

    with pytest.raises(
        ValueError,
        match="User ID must be greater than zero."
    ):
        WishlistService.validate_user_id(0)


def test_negative_user_id():
    """Test negative user ID."""

    with pytest.raises(
        ValueError,
        match="User ID must be greater than zero."
    ):
        WishlistService.validate_user_id(-1)


def test_validate_product_id():
    """Test valid product ID."""

    WishlistService.validate_product_id(1)


def test_invalid_product_id():
    """Test invalid product ID."""

    with pytest.raises(
        ValueError,
        match="Product ID must be greater than zero."
    ):
        WishlistService.validate_product_id(0)


def test_negative_product_id():
    """Test negative product ID."""

    with pytest.raises(
        ValueError,
        match="Product ID must be greater than zero."
    ):
        WishlistService.validate_product_id(-1)


def test_validate_wishlist_id():
    """Test valid wishlist ID."""

    WishlistService.validate_wishlist_id(1)


def test_invalid_wishlist_id():
    """Test invalid wishlist ID."""

    with pytest.raises(
        ValueError,
        match="Wishlist ID must be greater than zero."
    ):
        WishlistService.validate_wishlist_id(0)


def test_negative_wishlist_id():
    """Test negative wishlist ID."""

    with pytest.raises(
        ValueError,
        match="Wishlist ID must be greater than zero."
    ):
        WishlistService.validate_wishlist_id(-1)


# ============================================================
# GET WISHLIST
# ============================================================

def test_get_wishlist():
    """Test retrieving a user's wishlist."""

    user, product = create_user_and_product()

    try:
        result = WishlistService.get_wishlist(
            user.user_id
        )

        assert isinstance(result, list)
        assert result == []

    finally:
        cleanup_user_and_product(
            user.user_id,
            product.product_id
        )


def test_get_wishlist_invalid_user():
    """Test retrieving wishlist with invalid user ID."""

    with pytest.raises(
        ValueError,
        match="User ID must be greater than zero."
    ):
        WishlistService.get_wishlist(0)


# ============================================================
# ADD TO WISHLIST
# ============================================================

def test_add_to_wishlist():
    """Test adding a product to a wishlist."""

    user, product = create_user_and_product()

    try:
        result = WishlistService.add_to_wishlist(
            user.user_id,
            product.product_id
        )

        assert result is True

        wishlist_item = (
            WishlistService.get_product_from_wishlist(
                user.user_id,
                product.product_id
            )
        )

        assert wishlist_item is not None
        assert wishlist_item.user_id == user.user_id
        assert wishlist_item.product_id == product.product_id

    finally:
        cleanup_user_and_product(
            user.user_id,
            product.product_id
        )


def test_add_to_wishlist_invalid_user():
    """Test adding with invalid user ID."""

    with pytest.raises(
        ValueError,
        match="User ID must be greater than zero."
    ):
        WishlistService.add_to_wishlist(
            0,
            1
        )


def test_add_to_wishlist_invalid_product():
    """Test adding with invalid product ID."""

    with pytest.raises(
        ValueError,
        match="Product ID must be greater than zero."
    ):
        WishlistService.add_to_wishlist(
            1,
            0
        )


def test_add_to_wishlist_product_not_found():
    """Test adding a nonexistent product."""

    user = UserRepository.create(
        create_test_user()
    )

    assert user is not None

    try:
        with pytest.raises(
            ValueError,
            match="Product not found."
        ):
            WishlistService.add_to_wishlist(
                user.user_id,
                999999999
            )

    finally:
        UserRepository.delete(
            user.user_id
        )


def test_add_duplicate_product_to_wishlist():
    """Test that duplicate wishlist entries are rejected."""

    user, product = create_user_and_product()

    try:
        first_result = (
            WishlistService.add_to_wishlist(
                user.user_id,
                product.product_id
            )
        )

        assert first_result is True

        with pytest.raises(
            ValueError,
            match="Product is already in the wishlist."
        ):
            WishlistService.add_to_wishlist(
                user.user_id,
                product.product_id
            )

    finally:
        cleanup_user_and_product(
            user.user_id,
            product.product_id
        )


# ============================================================
# REMOVE FROM WISHLIST
# ============================================================

def test_remove_from_wishlist():
    """Test removing a product from a wishlist."""

    user, product = create_user_and_product()

    try:
        WishlistService.add_to_wishlist(
            user.user_id,
            product.product_id
        )

        result = (
            WishlistService.remove_from_wishlist(
                user.user_id,
                product.product_id
            )
        )

        assert result is True

        wishlist_item = (
            WishlistService.get_product_from_wishlist(
                user.user_id,
                product.product_id
            )
        )

        assert wishlist_item is None

    finally:
        cleanup_user_and_product(
            user.user_id,
            product.product_id
        )


def test_remove_from_wishlist_invalid_user():
    """Test removing with invalid user ID."""

    with pytest.raises(
        ValueError,
        match="User ID must be greater than zero."
    ):
        WishlistService.remove_from_wishlist(
            0,
            1
        )


def test_remove_from_wishlist_invalid_product():
    """Test removing with invalid product ID."""

    with pytest.raises(
        ValueError,
        match="Product ID must be greater than zero."
    ):
        WishlistService.remove_from_wishlist(
            1,
            0
        )


def test_remove_product_not_in_wishlist():
    """Test removing a product that is not in wishlist."""

    user, product = create_user_and_product()

    try:
        with pytest.raises(
            ValueError,
            match="Product is not in the wishlist."
        ):
            WishlistService.remove_from_wishlist(
                user.user_id,
                product.product_id
            )

    finally:
        cleanup_user_and_product(
            user.user_id,
            product.product_id
        )


# ============================================================
# CLEAR WISHLIST
# ============================================================

def test_clear_wishlist():
    """Test clearing a user's wishlist."""

    user, product = create_user_and_product()

    try:
        WishlistService.add_to_wishlist(
            user.user_id,
            product.product_id
        )

        result = WishlistService.clear_wishlist(
            user.user_id
        )

        assert result is True

        wishlist = WishlistService.get_wishlist(
            user.user_id
        )

        assert wishlist == []

    finally:
        cleanup_user_and_product(
            user.user_id,
            product.product_id
        )


def test_clear_empty_wishlist():
    """Test clearing an empty wishlist."""

    user, product = create_user_and_product()

    try:
        result = WishlistService.clear_wishlist(
            user.user_id
        )

        assert result is False

    finally:
        cleanup_user_and_product(
            user.user_id,
            product.product_id
        )


def test_clear_wishlist_invalid_user():
    """Test clearing wishlist with invalid user ID."""

    with pytest.raises(
        ValueError,
        match="User ID must be greater than zero."
    ):
        WishlistService.clear_wishlist(0)


# ============================================================
# GET WISHLIST ITEM
# ============================================================

def test_get_wishlist_item():
    """Test retrieving a wishlist item by ID."""

    user, product = create_user_and_product()

    try:
        WishlistService.add_to_wishlist(
            user.user_id,
            product.product_id
        )

        item = (
            WishlistService.get_product_from_wishlist(
                user.user_id,
                product.product_id
            )
        )

        assert item is not None

        result = WishlistService.get_wishlist_item(
            item.wishlist_id
        )

        assert result is not None
        assert result.wishlist_id == item.wishlist_id
        assert result.user_id == user.user_id
        assert result.product_id == product.product_id

    finally:
        cleanup_user_and_product(
            user.user_id,
            product.product_id
        )


def test_get_wishlist_item_invalid_id():
    """Test retrieving a wishlist item with invalid ID."""

    with pytest.raises(
        ValueError,
        match="Wishlist ID must be greater than zero."
    ):
        WishlistService.get_wishlist_item(0)


def test_get_wishlist_item_not_found():
    """Test retrieving a nonexistent wishlist item."""

    result = WishlistService.get_wishlist_item(
        999999999
    )

    assert result is None


# ============================================================
# GET PRODUCT FROM WISHLIST
# ============================================================

def test_get_product_from_wishlist():
    """Test retrieving a specific wishlist product."""

    user, product = create_user_and_product()

    try:
        WishlistService.add_to_wishlist(
            user.user_id,
            product.product_id
        )

        result = (
            WishlistService.get_product_from_wishlist(
                user.user_id,
                product.product_id
            )
        )

        assert result is not None
        assert result.user_id == user.user_id
        assert result.product_id == product.product_id

    finally:
        cleanup_user_and_product(
            user.user_id,
            product.product_id
        )


def test_get_product_from_wishlist_invalid_user():
    """Test invalid user ID."""

    with pytest.raises(
        ValueError,
        match="User ID must be greater than zero."
    ):
        WishlistService.get_product_from_wishlist(
            0,
            1
        )


def test_get_product_from_wishlist_invalid_product():
    """Test invalid product ID."""

    with pytest.raises(
        ValueError,
        match="Product ID must be greater than zero."
    ):
        WishlistService.get_product_from_wishlist(
            1,
            0
        )


# ============================================================
# IS PRODUCT IN WISHLIST
# ============================================================

def test_is_product_in_wishlist():
    """Test checking whether a product is in wishlist."""

    user, product = create_user_and_product()

    try:
        result_before = (
            WishlistService.is_product_in_wishlist(
                user.user_id,
                product.product_id
            )
        )

        assert result_before is False

        WishlistService.add_to_wishlist(
            user.user_id,
            product.product_id
        )

        result_after = (
            WishlistService.is_product_in_wishlist(
                user.user_id,
                product.product_id
            )
        )

        assert result_after is True

    finally:
        cleanup_user_and_product(
            user.user_id,
            product.product_id
        )


def test_is_product_in_wishlist_invalid_user():
    """Test checking wishlist with invalid user ID."""

    with pytest.raises(
        ValueError,
        match="User ID must be greater than zero."
    ):
        WishlistService.is_product_in_wishlist(
            0,
            1
        )


def test_is_product_in_wishlist_invalid_product():
    """Test checking wishlist with invalid product ID."""

    with pytest.raises(
        ValueError,
        match="Product ID must be greater than zero."
    ):
        WishlistService.is_product_in_wishlist(
            1,
            0
        )