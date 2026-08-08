"""
product_service.py
------------------
Business logic related to products.
"""

from typing import Optional

from models.product import Product
from repositories.product_repository import ProductRepository


class ProductService:
    """Provides business operations for products."""

    @staticmethod
    def validate_product(
        category_id: int,
        name: str,
        price: float,
        stock: int
    ) -> None:
        """
        Validate product information.

        Raises:
            ValueError: If product information is invalid.
        """

        if category_id <= 0:
            raise ValueError(
                "Category ID must be greater than zero."
            )

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
    def is_available(
        product: Product
    ) -> bool:
        """
        Check whether a product is available.

        Returns:
            True if product stock is greater than zero.
        """

        return product.stock > 0

    @staticmethod
    def increase_stock(
        product: Product,
        quantity: int
    ) -> None:
        """
        Increase product stock.

        Args:
            product: Product whose stock should increase.
            quantity: Quantity to add.

        Raises:
            ValueError: If quantity is invalid.
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

        Args:
            product: Product whose stock should decrease.
            quantity: Quantity to remove.

        Raises:
            ValueError: If quantity is invalid or
                        stock is insufficient.
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

    @staticmethod
    def create_product(
        product: Product
    ) -> Optional[Product]:
        """
        Validate and create a product in the database.

        Args:
            product: Product object to create.

        Returns:
            Created Product object or None if database
            connection fails.
        """

        ProductService.validate_product(
            category_id=product.category_id or 0,
            name=product.name,
            price=product.price,
            stock=product.stock
        )

        product.name = product.name.strip()
        product.description = product.description.strip()
        product.image_url = product.image_url.strip()

        return ProductRepository.create(product)

    @staticmethod
    def get_product(
        product_id: int
    ) -> Optional[Product]:
        """
        Get a product by its ID.

        Args:
            product_id: ID of the product.

        Returns:
            Product object or None if not found.

        Raises:
            ValueError: If product ID is invalid.
        """

        if product_id <= 0:
            raise ValueError(
                "Product ID must be greater than zero."
            )

        return ProductRepository.get_by_id(
            product_id
        )

    @staticmethod
    def get_all_products() -> list[Product]:
        """
        Get all products.

        Returns:
            List of Product objects.
        """

        return ProductRepository.get_all()

    @staticmethod
    def update_product(
        product: Product
    ) -> bool:
        """
        Validate and update an existing product.

        Args:
            product: Product object to update.

        Returns:
            True if the product was updated successfully.

        Raises:
            ValueError: If product ID or product data
                        is invalid.
        """

        if product.product_id is None:
            raise ValueError(
                "Product ID is required."
            )

        ProductService.validate_product(
            category_id=product.category_id or 0,
            name=product.name,
            price=product.price,
            stock=product.stock
        )

        product.name = product.name.strip()
        product.description = product.description.strip()
        product.image_url = product.image_url.strip()

        return ProductRepository.update(
            product
        )

    @staticmethod
    def delete_product(
        product_id: int
    ) -> bool:
        """
        Delete a product.

        Args:
            product_id: ID of the product to delete.

        Returns:
            True if the product was deleted successfully.

        Raises:
            ValueError: If product ID is invalid.
        """

        if product_id <= 0:
            raise ValueError(
                "Product ID must be greater than zero."
            )

        return ProductRepository.delete(
            product_id
        )