"""
category.py
-----------
Defines the Category model for the PyCommerce project.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Category:
    """
    Represents a product category in PyCommerce.
    """

    category_id: Optional[int] = None
    name: str = ""
    description: str = ""
    created_at: Optional[str] = None

    def __str__(self) -> str:
        """Return a readable representation of the category."""

        return (
            f"Category("
            f"id={self.category_id}, "
            f"name='{self.name}'"
            f")"
        )