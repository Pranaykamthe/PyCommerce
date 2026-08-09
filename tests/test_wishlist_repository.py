"""
Integration tests for WishlistRepository.
"""

import uuid

from models.wishlist import Wishlist
from models.product import Product
from models.user import User

from repositories.wishlist_repository import WishlistRepository
from repositories.product_repository import ProductRepository
from repositories.user_repository import UserRepository
from services.auth_service import AuthService


def create_test_user() -> User:
    """Create a temporary test user."""

    email = (
        f"wishlist_repo_{uuid.uuid4().hex[:10]}"
        "@pycommerce.test"
    )

    return User(
        name="Wishlist Repository Test",
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
            f"Wishlist Test Product "
            f"{uuid.uuid4().hex[:8]}"
        ),
        description="Wishlist repository test product",
        price=500.00,
        stock=20,
        image_url="wishlist-test.jpg"
    )


def test_create_wishlist_item():
    """Test creating a wishlist item."""

    user = UserRepository.create(
        create_test_user()
    )

    assert user is not None

    product = ProductRepository.create(
        create_test_product()
    )

    assert product is not None

    wishlist = Wishlist(
        user_id=user.user_id,
        product_id=product.product_id
    )

    created = WishlistRepository.create(
        wishlist
    )

    assert created is not None
    assert created.wishlist_id is not None
    assert created.user_id == user.user_id
    assert created.product_id == product.product_id

    WishlistRepository.delete(
        created.wishlist_id
    )

    ProductRepository.delete(
        product.product_id
    )

    UserRepository.delete(
        user.user_id
    )


def test_get_wishlist_by_id():
    """Test retrieving a wishlist item by ID."""

    user = UserRepository.create(
        create_test_user()
    )

    assert user is not None

    product = ProductRepository.create(
        create_test_product()
    )

    assert product is not None

    wishlist = Wishlist(
        user_id=user.user_id,
        product_id=product.product_id
    )

    created = WishlistRepository.create(
        wishlist
    )

    assert created is not None

    retrieved = WishlistRepository.get_by_id(
        created.wishlist_id
    )

    assert retrieved is not None
    assert retrieved.wishlist_id == created.wishlist_id
    assert retrieved.user_id == user.user_id
    assert retrieved.product_id == product.product_id

    WishlistRepository.delete(
        created.wishlist_id
    )

    ProductRepository.delete(
        product.product_id
    )

    UserRepository.delete(
        user.user_id
    )


def test_get_wishlist_by_id_not_found():
    """Test retrieving a nonexistent wishlist item."""

    result = WishlistRepository.get_by_id(
        999999999
    )

    assert result is None


def test_get_by_user_and_product():
    """Test finding a user's specific wishlist product."""

    user = UserRepository.create(
        create_test_user()
    )

    assert user is not None

    product = ProductRepository.create(
        create_test_product()
    )

    assert product is not None

    wishlist = Wishlist(
        user_id=user.user_id,
        product_id=product.product_id
    )

    created = WishlistRepository.create(
        wishlist
    )

    assert created is not None

    result = (
        WishlistRepository.get_by_user_and_product(
            user.user_id,
            product.product_id
        )
    )

    assert result is not None
    assert result.wishlist_id == created.wishlist_id
    assert result.user_id == user.user_id
    assert result.product_id == product.product_id

    WishlistRepository.delete(
        created.wishlist_id
    )

    ProductRepository.delete(
        product.product_id
    )

    UserRepository.delete(
        user.user_id
    )


def test_get_by_user_and_product_not_found():
    """Test when a product is not in the user's wishlist."""

    user = UserRepository.create(
        create_test_user()
    )

    assert user is not None

    product = ProductRepository.create(
        create_test_product()
    )

    assert product is not None

    result = (
        WishlistRepository.get_by_user_and_product(
            user.user_id,
            product.product_id
        )
    )

    assert result is None

    ProductRepository.delete(
        product.product_id
    )

    UserRepository.delete(
        user.user_id
    )


def test_get_by_user():
    """Test retrieving all wishlist items for a user."""

    user = UserRepository.create(
        create_test_user()
    )

    assert user is not None

    product = ProductRepository.create(
        create_test_product()
    )

    assert product is not None

    wishlist = Wishlist(
        user_id=user.user_id,
        product_id=product.product_id
    )

    created = WishlistRepository.create(
        wishlist
    )

    assert created is not None

    items = WishlistRepository.get_by_user(
        user.user_id
    )

    assert isinstance(items, list)
    assert len(items) >= 1

    found = any(
        item.wishlist_id == created.wishlist_id
        for item in items
    )

    assert found is True

    WishlistRepository.delete(
        created.wishlist_id
    )

    ProductRepository.delete(
        product.product_id
    )

    UserRepository.delete(
        user.user_id
    )


def test_get_by_user_empty():
    """Test retrieving an empty wishlist."""

    user = UserRepository.create(
        create_test_user()
    )

    assert user is not None

    items = WishlistRepository.get_by_user(
        user.user_id
    )

    assert isinstance(items, list)
    assert len(items) == 0

    UserRepository.delete(
        user.user_id
    )


def test_delete_wishlist_item():
    """Test deleting a wishlist item."""

    user = UserRepository.create(
        create_test_user()
    )

    assert user is not None

    product = ProductRepository.create(
        create_test_product()
    )

    assert product is not None

    wishlist = Wishlist(
        user_id=user.user_id,
        product_id=product.product_id
    )

    created = WishlistRepository.create(
        wishlist
    )

    assert created is not None

    result = WishlistRepository.delete(
        created.wishlist_id
    )

    assert result is True

    deleted = WishlistRepository.get_by_id(
        created.wishlist_id
    )

    assert deleted is None

    ProductRepository.delete(
        product.product_id
    )

    UserRepository.delete(
        user.user_id
    )


def test_delete_wishlist_item_not_found():
    """Test deleting a nonexistent wishlist item."""

    result = WishlistRepository.delete(
        999999999
    )

    assert result is False


def test_clear_user_wishlist():
    """Test clearing all wishlist items for a user."""

    user = UserRepository.create(
        create_test_user()
    )

    assert user is not None

    product_1 = ProductRepository.create(
        create_test_product()
    )

    assert product_1 is not None

    product_2 = ProductRepository.create(
        create_test_product()
    )

    assert product_2 is not None

    wishlist_1 = Wishlist(
        user_id=user.user_id,
        product_id=product_1.product_id
    )

    wishlist_2 = Wishlist(
        user_id=user.user_id,
        product_id=product_2.product_id
    )

    created_1 = WishlistRepository.create(
        wishlist_1
    )

    created_2 = WishlistRepository.create(
        wishlist_2
    )

    assert created_1 is not None
    assert created_2 is not None

    result = WishlistRepository.clear_user_wishlist(
        user.user_id
    )

    assert result is True

    items = WishlistRepository.get_by_user(
        user.user_id
    )

    assert len(items) == 0

    ProductRepository.delete(
        product_1.product_id
    )

    ProductRepository.delete(
        product_2.product_id
    )

    UserRepository.delete(
        user.user_id
    )


def test_clear_user_wishlist_empty():
    """Test clearing an already empty wishlist."""

    user = UserRepository.create(
        create_test_user()
    )

    assert user is not None

    result = WishlistRepository.clear_user_wishlist(
        user.user_id
    )

    assert result is False

    UserRepository.delete(
        user.user_id
    )