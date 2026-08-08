"""
product_service.py
------------------
Business logic related to products.
"""

from models.product import Product


class ProductService:
    """Provides business operations for products."""

    @staticmethod
    def validate_product(
        name: str,
        price: float,
        stock: int
    ) -> None:
        """
        Validate product information.

        Raises:
            ValueError: If product information is invalid.
        """

        if not name or not name.strip():
            raise ValueError(
                "Product name cannot be empty."
            )

        if price < 0:
            raise ValueError(
                "Product price cannot be negative."
            )

        if stock < 0:
            raise ValueError(
                "Product stock cannot be negative."
            )

    @staticmethod
    def is_available(product: Product) -> bool:
        """
        Check whether a product is available.

        Returns:
            True if stock is greater than zero.
        """

        return product.stock > 0

    @staticmethod
    def increase_stock(
        product: Product,
        quantity: int
    ) -> None:
        """
        Increase product stock.
        """

        if quantity <= 0:
            raise ValueError(
                "Quantity must be greater than zero."
            )

        product.stock += quantity

    @staticmethod
    def decrease_stock(
        product: Product,
        quantity: int
    ) -> None:
        """
        Decrease product stock.
        """

        if quantity <= 0:
            raise ValueError(
                "Quantity must be greater than zero."
            )

        if quantity > product.stock:
            raise ValueError(
                "Insufficient stock."
            )

        product.stock -= quantity