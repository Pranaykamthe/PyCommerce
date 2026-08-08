"""
product.py
----------
Defines the Product model for the PyCommerce project.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Product:
    """
    Represents a product in the PyCommerce store.
    """

    product_id: Optional[int] = None
    category_id: Optional[int] = None
    name: str = ""
    description: str = ""
    price: float = 0.0
    stock: int = 0
    image_url: str = ""
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def __str__(self) -> str:
        """Return a readable representation of the product."""

        return (
            f"Product("
            f"id={self.product_id}, "
            f"name='{self.name}', "
            f"price={self.price}, "
            f"stock={self.stock}"
            f")"
        )