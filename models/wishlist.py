"""
Defines the Wishlist model for the PyCommerce project.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Wishlist:
    """
    Represents a product saved by a customer
    in their wishlist.
    """

    wishlist_id: Optional[int] = None
    user_id: Optional[int] = None
    product_id: Optional[int] = None
    added_at: Optional[str] = None

    def __str__(self) -> str:
        """Return a readable representation of the wishlist item."""

        return (
            f"Wishlist("
            f"id={self.wishlist_id}, "
            f"user_id={self.user_id}, "
            f"product_id={self.product_id}"
            f")"
        )