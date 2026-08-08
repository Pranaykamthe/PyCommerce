"""
order_service.py
----------------
Business logic related to orders and order items.
"""

from typing import Optional

from models.order import Order
from models.order_item import OrderItem
from repositories.order_repository import OrderRepository


class OrderService:
    """Provides business operations for orders."""

    ALLOWED_STATUSES = {
        "pending",
        "confirmed",
        "shipped",
        "delivered",
        "cancelled"
    }

    # ========================================================
    # Validation
    # ========================================================

    @staticmethod
    def validate_user_id(
        user_id: Optional[int]
    ) -> None:
        """Validate user ID."""

        if user_id is None or user_id <= 0:
            raise ValueError(
                "Valid user ID is required."
            )

    @staticmethod
    def validate_status(
        status: str
    ) -> None:
        """Validate order status."""

        if status not in OrderService.ALLOWED_STATUSES:
            raise ValueError(
                "Invalid order status."
            )

    @staticmethod
    def validate_shipping_address(
        shipping_address: str
    ) -> None:
        """Validate shipping address."""

        if (
            not shipping_address
            or not shipping_address.strip()
        ):
            raise ValueError(
                "Shipping address cannot be empty."
            )

    @staticmethod
    def validate_quantity(
        quantity: int
    ) -> None:
        """Validate order item quantity."""

        if quantity <= 0:
            raise ValueError(
                "Quantity must be greater than zero."
            )

    @staticmethod
    def validate_price(
        price: float
    ) -> None:
        """Validate product price."""

        if price < 0:
            raise ValueError(
                "Price cannot be negative."
            )

    # ========================================================
    # Order Creation
    # ========================================================

    @staticmethod
    def calculate_total(
        items: list[OrderItem]
    ) -> float:
        """
        Calculate the total amount of an order.

        Total = sum(quantity × unit price)
        """

        if not items:
            raise ValueError(
                "Order must contain at least one item."
            )

        total = 0.0

        for item in items:
            OrderService.validate_quantity(
                item.quantity
            )

            OrderService.validate_price(
                item.price
            )

            total += (
                item.quantity *
                item.price
            )

        return round(total, 2)

    @staticmethod
    def create_order(
        order: Order,
        items: list[OrderItem]
    ) -> Optional[Order]:
        """
        Validate and create an order with its items.

        The order total is calculated from the items.
        """

        OrderService.validate_user_id(
            order.user_id
        )

        OrderService.validate_status(
            order.status
        )

        OrderService.validate_shipping_address(
            order.shipping_address
        )

        if not items:
            raise ValueError(
                "Order must contain at least one item."
            )

        total = OrderService.calculate_total(
            items
        )

        order.total_amount = total
        order.shipping_address = (
            order.shipping_address.strip()
        )

        created_order = (
            OrderRepository.create_order(order)
        )

        if created_order is None:
            return None

        created_items = []

        try:
            for item in items:
                item.order_id = (
                    created_order.order_id
                )

                created_item = (
                    OrderRepository.create_order_item(
                        item
                    )
                )

                if created_item is None:
                    raise RuntimeError(
                        "Failed to create order item."
                    )

                created_items.append(
                    created_item
                )

        except Exception:
            # Clean up the order if an item fails.
            if created_order.order_id is not None:
                OrderRepository.delete_order(
                    created_order.order_id
                )

            raise

        return created_order

    # ========================================================
    # Get Orders
    # ========================================================

    @staticmethod
    def get_order(
        order_id: int
    ) -> Optional[Order]:
        """Get an order by ID."""

        if order_id <= 0:
            raise ValueError(
                "Order ID must be greater than zero."
            )

        return OrderRepository.get_order_by_id(
            order_id
        )

    @staticmethod
    def get_user_orders(
        user_id: int
    ) -> list[Order]:
        """Get all orders belonging to a user."""

        OrderService.validate_user_id(
            user_id
        )

        return OrderRepository.get_orders_by_user(
            user_id
        )

    @staticmethod
    def get_order_items(
        order_id: int
    ) -> list[OrderItem]:
        """Get all items belonging to an order."""

        if order_id <= 0:
            raise ValueError(
                "Order ID must be greater than zero."
            )

        return OrderRepository.get_order_items(
            order_id
        )

    # ========================================================
    # Update Order
    # ========================================================

    @staticmethod
    def update_order(
        order: Order
    ) -> bool:
        """Validate and update an order."""

        if order.order_id is None:
            raise ValueError(
                "Order ID is required."
            )

        OrderService.validate_user_id(
            order.user_id
        )

        OrderService.validate_status(
            order.status
        )

        OrderService.validate_shipping_address(
            order.shipping_address
        )

        if order.total_amount < 0:
            raise ValueError(
                "Order total cannot be negative."
            )

        order.shipping_address = (
            order.shipping_address.strip()
        )

        return OrderRepository.update_order(
            order
        )

    # ========================================================
    # Update Order Status
    # ========================================================

    @staticmethod
    def update_order_status(
        order_id: int,
        status: str
    ) -> bool:
        """
        Update only the status of an order.
        """

        if order_id <= 0:
            raise ValueError(
                "Order ID must be greater than zero."
            )

        OrderService.validate_status(
            status
        )

        order = OrderRepository.get_order_by_id(
            order_id
        )

        if order is None:
            return False

        order.status = status

        return OrderRepository.update_order(
            order
        )

    # ========================================================
    # Order Item Operations
    # ========================================================

    @staticmethod
    def add_order_item(
        item: OrderItem
    ) -> Optional[OrderItem]:
        """Validate and add an order item."""

        if item.order_id is None or item.order_id <= 0:
            raise ValueError(
                "Valid order ID is required."
            )

        if item.product_id is None or item.product_id <= 0:
            raise ValueError(
                "Valid product ID is required."
            )

        OrderService.validate_quantity(
            item.quantity
        )

        OrderService.validate_price(
            item.price
        )

        return OrderRepository.create_order_item(
            item
        )

    @staticmethod
    def update_order_item(
        item: OrderItem
    ) -> bool:
        """Validate and update an order item."""

        if item.order_item_id is None:
            raise ValueError(
                "Order item ID is required."
            )

        if item.product_id is None or item.product_id <= 0:
            raise ValueError(
                "Valid product ID is required."
            )

        OrderService.validate_quantity(
            item.quantity
        )

        OrderService.validate_price(
            item.price
        )

        return OrderRepository.update_order_item(
            item
        )

    @staticmethod
    def delete_order_item(
        order_item_id: int
    ) -> bool:
        """Delete an order item."""

        if order_item_id <= 0:
            raise ValueError(
                "Order item ID must be greater than zero."
            )

        return OrderRepository.delete_order_item(
            order_item_id
        )

    # ========================================================
    # Delete Order
    # ========================================================

    @staticmethod
    def delete_order(
        order_id: int
    ) -> bool:
        """Delete an order and its items."""

        if order_id <= 0:
            raise ValueError(
                "Order ID must be greater than zero."
            )

        return OrderRepository.delete_order(
            order_id
        )