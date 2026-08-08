"""
order_service.py
----------------
Business logic related to orders.
"""


class OrderService:
    """Provides business operations for orders."""

    @staticmethod
    def validate_quantity(quantity: int) -> None:
        """Validate an order item quantity."""

        if quantity <= 0:
            raise ValueError(
                "Quantity must be greater than zero."
            )

    @staticmethod
    def calculate_item_total(
        price: float,
        quantity: int
    ) -> float:
        """Calculate the total price of one order item."""

        if price < 0:
            raise ValueError(
                "Price cannot be negative."
            )

        OrderService.validate_quantity(quantity)

        return price * quantity

    @staticmethod
    def calculate_order_total(
        item_totals: list[float]
    ) -> float:
        """Calculate the total value of an order."""

        if not item_totals:
            raise ValueError(
                "Order must contain at least one item."
            )

        for item_total in item_totals:
            if item_total < 0:
                raise ValueError(
                    "Item total cannot be negative."
                )

        return sum(item_totals)

    @staticmethod
    def validate_order(
        customer_id: int,
        item_totals: list[float]
    ) -> None:
        """Validate order information."""

        if customer_id <= 0:
            raise ValueError(
                "Invalid customer ID."
            )

        if not item_totals:
            raise ValueError(
                "Order must contain at least one item."
            )