"""
Business logic related to shopping carts.
"""

from typing import Optional

from models.cart import Cart
from repositories.cart_repository import CartRepository
from repositories.product_repository import ProductRepository


class CartService:
    """Provides business operations for shopping carts."""

    # ========================================================
    # Validation
    # ========================================================

    @staticmethod
    def validate_user_id(
        user_id: int
    ) -> None:
        """Validate a user ID."""

        if user_id <= 0:
            raise ValueError(
                "User ID must be greater than zero."
            )

    @staticmethod
    def validate_product_id(
        product_id: int
    ) -> None:
        """Validate a product ID."""

        if product_id <= 0:
            raise ValueError(
                "Product ID must be greater than zero."
            )

    @staticmethod
    def validate_quantity(
        quantity: int
    ) -> None:
        """Validate cart quantity."""

        if quantity <= 0:
            raise ValueError(
                "Quantity must be greater than zero."
            )

    @staticmethod
    def validate_cart_id(
        cart_id: int
    ) -> None:
        """Validate cart ID."""

        if cart_id <= 0:
            raise ValueError(
                "Cart ID must be greater than zero."
            )

    # ========================================================
    # Get Cart
    # ========================================================

    @staticmethod
    def get_cart(
        user_id: int
    ) -> list[Cart]:
        """
        Get all cart items belonging to a user.
        """

        CartService.validate_user_id(
            user_id
        )

        return CartRepository.get_by_user(
            user_id
        )

    # ========================================================
    # Add To Cart
    # ========================================================

    @staticmethod
    def add_to_cart(
        user_id: int,
        product_id: int,
        quantity: int
    ) -> bool:
        """
        Add a product to the user's cart.

        If the product already exists in the cart,
        its quantity is increased.

        The requested quantity cannot exceed
        the available product stock.
        """

        CartService.validate_user_id(
            user_id
        )

        CartService.validate_product_id(
            product_id
        )

        CartService.validate_quantity(
            quantity
        )

        # ----------------------------------------------------
        # Check product
        # ----------------------------------------------------

        product = ProductRepository.get_by_id(
            product_id
        )

        if product is None:
            raise ValueError(
                "Product not found."
            )

        if product.stock <= 0:
            raise ValueError(
                "Product is out of stock."
            )

        # ----------------------------------------------------
        # Check existing cart quantity
        # ----------------------------------------------------

        existing_item = (
            CartRepository.get_by_user_and_product(
                user_id=user_id,
                product_id=product_id
            )
        )

        current_quantity = 0

        if existing_item is not None:
            current_quantity = (
                existing_item.quantity
            )

        new_quantity = (
            current_quantity + quantity
        )

        if new_quantity > product.stock:
            raise ValueError(
                f"Only {product.stock} item(s) "
                "are available in stock."
            )

        # ----------------------------------------------------
        # Update existing item
        # ----------------------------------------------------

        if existing_item is not None:
            return CartRepository.update_quantity(
                cart_id=existing_item.cart_id,
                quantity=new_quantity
            )

        # ----------------------------------------------------
        # Create new cart item
        # ----------------------------------------------------

        cart = Cart(
            user_id=user_id,
            product_id=product_id,
            quantity=quantity
        )

        created_cart = CartRepository.create(
            cart
        )

        return created_cart is not None

    # ========================================================
    # Update Quantity
    # ========================================================

    @staticmethod
    def update_quantity(
        user_id: int,
        product_id: int,
        quantity: int
    ) -> bool:
        """
        Update the quantity of a product
        already present in the cart.
        """

        CartService.validate_user_id(
            user_id
        )

        CartService.validate_product_id(
            product_id
        )

        CartService.validate_quantity(
            quantity
        )

        # ----------------------------------------------------
        # Check product
        # ----------------------------------------------------

        product = ProductRepository.get_by_id(
            product_id
        )

        if product is None:
            raise ValueError(
                "Product not found."
            )

        if quantity > product.stock:
            raise ValueError(
                f"Only {product.stock} item(s) "
                "are available in stock."
            )

        # ----------------------------------------------------
        # Check cart item
        # ----------------------------------------------------

        existing_item = (
            CartRepository.get_by_user_and_product(
                user_id=user_id,
                product_id=product_id
            )
        )

        if existing_item is None:
            raise ValueError(
                "Product is not in the cart."
            )

        return CartRepository.update_quantity(
            cart_id=existing_item.cart_id,
            quantity=quantity
        )

    # ========================================================
    # Remove From Cart
    # ========================================================

    @staticmethod
    def remove_from_cart(
        user_id: int,
        product_id: int
    ) -> bool:
        """
        Remove a product from the user's cart.
        """

        CartService.validate_user_id(
            user_id
        )

        CartService.validate_product_id(
            product_id
        )

        existing_item = (
            CartRepository.get_by_user_and_product(
                user_id=user_id,
                product_id=product_id
            )
        )

        if existing_item is None:
            raise ValueError(
                "Product is not in the cart."
            )

        return CartRepository.delete(
            existing_item.cart_id
        )

    # ========================================================
    # Clear Cart
    # ========================================================

    @staticmethod
    def clear_cart(
        user_id: int
    ) -> bool:
        """
        Remove all items from the user's cart.

        Returns:
            True if one or more items were removed.
            False if the cart was already empty.
        """

        CartService.validate_user_id(
            user_id
        )

        return CartRepository.clear_user_cart(
            user_id
        )

    # ========================================================
    # Get Cart Item
    # ========================================================

    @staticmethod
    def get_cart_item(
        cart_id: int
    ) -> Optional[Cart]:
        """
        Get a cart item by cart ID.

        Raises:
            ValueError: If cart ID is invalid.
        """

        CartService.validate_cart_id(
            cart_id
        )

        return CartRepository.get_by_id(
            cart_id
        )

    # ========================================================
    # Get Product From Cart
    # ========================================================

    @staticmethod
    def get_product_from_cart(
        user_id: int,
        product_id: int
    ) -> Optional[Cart]:
        """
        Get a specific product from a user's cart.

        Raises:
            ValueError: If user ID or product ID is invalid.
        """

        CartService.validate_user_id(
            user_id
        )

        CartService.validate_product_id(
            product_id
        )

        return CartRepository.get_by_user_and_product(
            user_id,
            product_id
        )