"""
user.py
-------
Defines the User model for the PyCommerce project.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    """
    Represents a customer/admin user in PyCommerce.
    """

    user_id: Optional[int] = None
    name: str = ""
    email: str = ""
    password: str = ""
    phone: str = ""
    address: str = ""
    role: str = "customer"
    created_at: Optional[str] = None

    def __str__(self) -> str:
        """Return a readable representation of the user."""

        return (
            f"User("
            f"id={self.user_id}, "
            f"name='{self.name}', "
            f"email='{self.email}', "
            f"role='{self.role}'"
            f")"
        )