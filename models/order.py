"""
order.py
--------
Defines the Order model for the PyCommerce project.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Order:
    """
    Represents an order placed by a user.
    """

    order_id: Optional[int] = None
    user_id: Optional[int] = None
    total_amount: float = 0.0
    status: str = "pending"
    shipping_address: str = ""
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def __str__(self) -> str:
        """Return a readable representation of the order."""

        return (
            f"Order("
            f"id={self.order_id}, "
            f"user_id={self.user_id}, "
            f"total={self.total_amount}, "
            f"status='{self.status}'"
            f")"
        )