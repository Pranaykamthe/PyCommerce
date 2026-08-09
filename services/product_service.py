"""
Business logic related to products.
"""

from typing import Optional

from models.product import Product
from repositories.product_repository import ProductRepository


class ProductService:
    """Provides business operations for products."""

    # ========================================================
    # Validation
    # ========================================================

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

    # ========================================================
    # Availability
    # ========================================================

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

    # ========================================================
    # Increase Stock
    # ========================================================

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

    # ========================================================
    # Decrease Stock
    # ========================================================

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

    # ========================================================
    # Create Product
    # ========================================================

    @staticmethod
    def create_product(
        product: Product
    ) -> Optional[Product]:
        """
        Validate and create a product in the database.
        """

        ProductService.validate_product(
            category_id=product.category_id or 0,
            name=product.name,
            price=product.price,
            stock=product.stock
        )

        product.name = product.name.strip()
        product.description = (
            product.description.strip()
        )
        product.image_url = (
            product.image_url.strip()
        )

        return ProductRepository.create(
            product
        )

    # ========================================================
    # Get Product
    # ========================================================

    @staticmethod
    def get_product(
        product_id: int
    ) -> Optional[Product]:
        """
        Get a product by its ID.
        """

        if product_id <= 0:
            raise ValueError(
                "Product ID must be greater than zero."
            )

        return ProductRepository.get_by_id(
            product_id
        )

    # ========================================================
    # Get All Products
    # ========================================================

    @staticmethod
    def get_all_products() -> list[Product]:
        """
        Get all products.
        """

        return ProductRepository.get_all()

    # ========================================================
    # Get Products By Category
    # ========================================================

    @staticmethod
    def get_products_by_category(
        category_id: int
    ) -> list[Product]:
        """
        Get all products belonging to a category.

        Raises:
            ValueError: If category ID is invalid.
        """

        if category_id <= 0:
            raise ValueError(
                "Category ID must be greater than zero."
            )

        return ProductRepository.get_by_category(
            category_id
        )
    # ========================================================
    # Search Products
    # ========================================================

    @staticmethod
    def search_products(
        search_term: str
    ) -> list[Product]:
        """
        Search products by name.

        Args:
            search_term: Text to search for.

        Returns:
            List of matching Product objects.

        Raises:
            ValueError: If search term is empty.
        """

        if not search_term or not search_term.strip():
            raise ValueError(
                "Search term cannot be empty."
            )

        return ProductRepository.search_by_name(
            search_term.strip()
        )

    # ========================================================
    # Update Product
    # ========================================================

    @staticmethod
    def update_product(
        product: Product
    ) -> bool:
        """
        Validate and update an existing product.
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
        product.description = (
            product.description.strip()
        )
        product.image_url = (
            product.image_url.strip()
        )

        return ProductRepository.update(
            product
        )

    # ========================================================
    # Delete Product
    # ========================================================

    @staticmethod
    def delete_product(
        product_id: int
    ) -> bool:
        """
        Delete a product.
        """

        if product_id <= 0:
            raise ValueError(
                "Product ID must be greater than zero."
            )

        return ProductRepository.delete(
            product_id
        )
