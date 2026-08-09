"""
Defines the Payment model for the PyCommerce project.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Payment:
    """
    Represents a payment associated with an order.
    """

    payment_id: Optional[int] = None
    order_id: Optional[int] = None
    amount: float = 0.0
    payment_method: str = ""
    transaction_id: str = ""
    status: str = "pending"
    paid_at: Optional[str] = None

    def __str__(self) -> str:
        """Return a readable representation of the payment."""

        return (
            f"Payment("
            f"id={self.payment_id}, "
            f"order_id={self.order_id}, "
            f"amount={self.amount}, "
            f"method='{self.payment_method}', "
            f"status='{self.status}'"
            f")"
        )