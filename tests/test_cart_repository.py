"""
test_cart_repository.py
-----------------------
Integration tests for CartRepository.
"""

import uuid

from models.cart import Cart
from models.product import Product
from models.user import User

from repositories.cart_repository import CartRepository
from repositories.product_repository import ProductRepository
from repositories.user_repository import UserRepository
from services.auth_service import AuthService


def create_test_user() -> User:
    """Create a temporary test user."""

    email = (
        f"cart_repo_{uuid.uuid4().hex[:10]}"
        "@pycommerce.test"
    )

    return User(
        name="Cart Repository Test",
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
        name=f"Cart Test Product "
             f"{uuid.uuid4().hex[:8]}",
        description="Cart repository test product",
        price=250.00,
        stock=20,
        image_url="cart-test.jpg"
    )


def test_create_cart_item():
    """Test creating a cart item."""

    user = UserRepository.create(
        create_test_user()
    )

    assert user is not None

    product = ProductRepository.create(
        create_test_product()
    )

    assert product is not None

    cart = Cart(
        user_id=user.user_id,
        product_id=product.product_id,
        quantity=2
    )

    created = CartRepository.create(cart)

    assert created is not None
    assert created.cart_id is not None
    assert created.user_id == user.user_id
    assert created.product_id == product.product_id
    assert created.quantity == 2

    CartRepository.delete(
        created.cart_id
    )

    ProductRepository.delete(
        product.product_id
    )

    UserRepository.delete(
        user.user_id
    )


def test_get_cart_by_id():
    """Test retrieving a cart item by ID."""

    user = UserRepository.create(
        create_test_user()
    )

    assert user is not None

    product = ProductRepository.create(
        create_test_product()
    )

    assert product is not None

    cart = Cart(
        user_id=user.user_id,
        product_id=product.product_id,
        quantity=3
    )

    created = CartRepository.create(cart)

    assert created is not None

    retrieved = CartRepository.get_by_id(
        created.cart_id
    )

    assert retrieved is not None
    assert retrieved.cart_id == created.cart_id
    assert retrieved.quantity == 3

    CartRepository.delete(
        created.cart_id
    )

    ProductRepository.delete(
        product.product_id
    )

    UserRepository.delete(
        user.user_id
    )


def test_get_by_user_and_product():
    """Test finding a user's specific product."""

    user = UserRepository.create(
        create_test_user()
    )

    assert user is not None

    product = ProductRepository.create(
        create_test_product()
    )

    assert product is not None

    cart = Cart(
        user_id=user.user_id,
        product_id=product.product_id,
        quantity=4
    )

    created = CartRepository.create(cart)

    assert created is not None

    result = (
        CartRepository.get_by_user_and_product(
            user.user_id,
            product.product_id
        )
    )

    assert result is not None
    assert result.cart_id == created.cart_id
    assert result.quantity == 4

    CartRepository.delete(
        created.cart_id
    )

    ProductRepository.delete(
        product.product_id
    )

    UserRepository.delete(
        user.user_id
    )


def test_get_by_user():
    """Test retrieving all cart items for a user."""

    user = UserRepository.create(
        create_test_user()
    )

    assert user is not None

    product = ProductRepository.create(
        create_test_product()
    )

    assert product is not None

    cart = Cart(
        user_id=user.user_id,
        product_id=product.product_id,
        quantity=2
    )

    created = CartRepository.create(cart)

    assert created is not None

    items = CartRepository.get_by_user(
        user.user_id
    )

    assert isinstance(items, list)
    assert len(items) >= 1

    found = any(
        item.cart_id == created.cart_id
        for item in items
    )

    assert found is True

    CartRepository.delete(
        created.cart_id
    )

    ProductRepository.delete(
        product.product_id
    )

    UserRepository.delete(
        user.user_id
    )


def test_update_quantity():
    """Test updating cart quantity."""

    user = UserRepository.create(
        create_test_user()
    )

    assert user is not None

    product = ProductRepository.create(
        create_test_product()
    )

    assert product is not None

    cart = Cart(
        user_id=user.user_id,
        product_id=product.product_id,
        quantity=2
    )

    created = CartRepository.create(cart)

    assert created is not None

    result = CartRepository.update_quantity(
        created.cart_id,
        7
    )

    assert result is True

    updated = CartRepository.get_by_id(
        created.cart_id
    )

    assert updated is not None
    assert updated.quantity == 7

    CartRepository.delete(
        created.cart_id
    )

    ProductRepository.delete(
        product.product_id
    )

    UserRepository.delete(
        user.user_id
    )


def test_delete_cart_item():
    """Test deleting a cart item."""

    user = UserRepository.create(
        create_test_user()
    )

    assert user is not None

    product = ProductRepository.create(
        create_test_product()
    )

    assert product is not None

    cart = Cart(
        user_id=user.user_id,
        product_id=product.product_id,
        quantity=1
    )

    created = CartRepository.create(cart)

    assert created is not None

    result = CartRepository.delete(
        created.cart_id
    )

    assert result is True

    deleted = CartRepository.get_by_id(
        created.cart_id
    )

    assert deleted is None

    ProductRepository.delete(
        product.product_id
    )

    UserRepository.delete(
        user.user_id
    )


def test_clear_user_cart():
    """Test clearing all cart items for a user."""

    user = UserRepository.create(
        create_test_user()
    )

    assert user is not None

    product = ProductRepository.create(
        create_test_product()
    )

    assert product is not None

    cart = Cart(
        user_id=user.user_id,
        product_id=product.product_id,
        quantity=2
    )

    created = CartRepository.create(cart)

    assert created is not None

    result = CartRepository.clear_user_cart(
        user.user_id
    )

    assert result is True

    items = CartRepository.get_by_user(
        user.user_id
    )

    assert len(items) == 0

    ProductRepository.delete(
        product.product_id
    )

    UserRepository.delete(
        user.user_id
    )