"""
review.py
---------
Defines the Review model for the PyCommerce project.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Review:
    """
    Represents a customer review for a product.
    """

    review_id: Optional[int] = None
    user_id: Optional[int] = None
    product_id: Optional[int] = None
    rating: int = 0
    comment: str = ""
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def __str__(self) -> str:
        """Return a readable representation of the review."""

        return (
            f"Review("
            f"id={self.review_id}, "
            f"user_id={self.user_id}, "
            f"product_id={self.product_id}, "
            f"rating={self.rating}"
            f")"
        )