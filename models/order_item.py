"""
order_item.py
-------------
Defines the OrderItem model for the PyCommerce project.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class OrderItem:
    """
    Represents an individual product within an order.
    """

    order_item_id: Optional[int] = None
    order_id: Optional[int] = None
    product_id: Optional[int] = None
    quantity: int = 1
    price: float = 0.0

    def __str__(self) -> str:
        """Return a readable representation of the order item."""

        return (
            f"OrderItem("
            f"id={self.order_item_id}, "
            f"order_id={self.order_id}, "
            f"product_id={self.product_id}, "
            f"quantity={self.quantity}, "
            f"price={self.price}"
            f")"
        )