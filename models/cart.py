"""
Defines the Cart model for the PyCommerce project.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Cart:
    """
    Represents an item in a user's shopping cart.
    """

    cart_id: Optional[int] = None
    user_id: Optional[int] = None
    product_id: Optional[int] = None
    quantity: int = 1
    price: float = 0.0
    added_at: Optional[str] = None
    updated_at: Optional[str] = None

    def __str__(self) -> str:
        """Return a readable representation of the cart item."""

        return (
            f"Cart("
            f"id={self.cart_id}, "
            f"user_id={self.user_id}, "
            f"product_id={self.product_id}, "
            f"quantity={self.quantity}, "
            f"price={self.price}"
            f")"
        )