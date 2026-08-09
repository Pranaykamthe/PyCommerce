"""
Business logic related to product wishlists.
"""

from typing import Optional

from models.wishlist import Wishlist
from repositories.wishlist_repository import WishlistRepository
from repositories.product_repository import ProductRepository


class WishlistService:
    """Provides business operations for product wishlists."""

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
    def validate_wishlist_id(
        wishlist_id: int
    ) -> None:
        """Validate a wishlist ID."""

        if wishlist_id <= 0:
            raise ValueError(
                "Wishlist ID must be greater than zero."
            )

    # ========================================================
    # Get Wishlist
    # ========================================================

    @staticmethod
    def get_wishlist(
        user_id: int
    ) -> list[Wishlist]:
        """
        Get all wishlist items belonging to a user.
        """

        WishlistService.validate_user_id(
            user_id
        )

        return WishlistRepository.get_by_user(
            user_id
        )

    # ========================================================
    # Add To Wishlist
    # ========================================================

    @staticmethod
    def add_to_wishlist(
        user_id: int,
        product_id: int
    ) -> bool:
        """
        Add a product to the user's wishlist.

        A product cannot be added more than once.
        """

        WishlistService.validate_user_id(
            user_id
        )

        WishlistService.validate_product_id(
            product_id
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

        # ----------------------------------------------------
        # Check existing wishlist item
        # ----------------------------------------------------

        existing_item = (
            WishlistRepository.get_by_user_and_product(
                user_id=user_id,
                product_id=product_id
            )
        )

        if existing_item is not None:
            raise ValueError(
                "Product is already in the wishlist."
            )

        # ----------------------------------------------------
        # Create wishlist item
        # ----------------------------------------------------

        wishlist = Wishlist(
            user_id=user_id,
            product_id=product_id
        )

        created_wishlist = WishlistRepository.create(
            wishlist
        )

        return created_wishlist is not None

    # ========================================================
    # Remove From Wishlist
    # ========================================================

    @staticmethod
    def remove_from_wishlist(
        user_id: int,
        product_id: int
    ) -> bool:
        """
        Remove a product from the user's wishlist.
        """

        WishlistService.validate_user_id(
            user_id
        )

        WishlistService.validate_product_id(
            product_id
        )

        existing_item = (
            WishlistRepository.get_by_user_and_product(
                user_id=user_id,
                product_id=product_id
            )
        )

        if existing_item is None:
            raise ValueError(
                "Product is not in the wishlist."
            )

        return WishlistRepository.delete(
            existing_item.wishlist_id
        )

    # ========================================================
    # Clear Wishlist
    # ========================================================

    @staticmethod
    def clear_wishlist(
        user_id: int
    ) -> bool:
        """
        Remove all products from the user's wishlist.

        Returns:
            True if one or more items were removed.
            False if the wishlist was already empty.
        """

        WishlistService.validate_user_id(
            user_id
        )

        return WishlistRepository.clear_user_wishlist(
            user_id
        )

    # ========================================================
    # Get Wishlist Item
    # ========================================================

    @staticmethod
    def get_wishlist_item(
        wishlist_id: int
    ) -> Optional[Wishlist]:
        """
        Get a wishlist item by wishlist ID.

        Raises:
            ValueError: If wishlist ID is invalid.
        """

        WishlistService.validate_wishlist_id(
            wishlist_id
        )

        return WishlistRepository.get_by_id(
            wishlist_id
        )

    # ========================================================
    # Get Product From Wishlist
    # ========================================================

    @staticmethod
    def get_product_from_wishlist(
        user_id: int,
        product_id: int
    ) -> Optional[Wishlist]:
        """
        Get a specific product from a user's wishlist.

        Raises:
            ValueError: If user ID or product ID is invalid.
        """

        WishlistService.validate_user_id(
            user_id
        )

        WishlistService.validate_product_id(
            product_id
        )

        return WishlistRepository.get_by_user_and_product(
            user_id,
            product_id
        )

    # ========================================================
    # Is Product In Wishlist
    # ========================================================

    @staticmethod
    def is_product_in_wishlist(
        user_id: int,
        product_id: int
    ) -> bool:
        """
        Check whether a product exists in a user's wishlist.
        """

        WishlistService.validate_user_id(
            user_id
        )

        WishlistService.validate_product_id(
            product_id
        )

        wishlist_item = (
            WishlistRepository.get_by_user_and_product(
                user_id,
                product_id
            )
        )

        return wishlist_item is not None