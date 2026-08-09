"""
Business logic related to categories.
"""

from typing import Optional

from models.category import Category
from repositories.category_repository import CategoryRepository


class CategoryService:
    """Provides business operations for categories."""

    # ========================================================
    # Validation
    # ========================================================

    @staticmethod
    def validate_category(
        name: str,
        description: str = ""
    ) -> None:
        """Validate category information."""

        if not name or not name.strip():

            raise ValueError(
                "Category name cannot be empty."
            )

    # ========================================================
    # Create Category
    # ========================================================

    @staticmethod
    def create_category(
        category: Category
    ) -> Optional[Category]:
        """Validate and create a category."""

        CategoryService.validate_category(
            name=category.name,
            description=category.description
        )

        category.name = category.name.strip()

        category.description = (
            category.description.strip()
            if category.description
            else ""
        )

        return CategoryRepository.create(
            category
        )

    # ========================================================
    # Get Category
    # ========================================================

    @staticmethod
    def get_category(
        category_id: int
    ) -> Optional[Category]:
        """Get an active category by ID."""

        if category_id <= 0:

            raise ValueError(
                "Category ID must be greater than zero."
            )

        return CategoryRepository.get_by_id(
            category_id
        )

    # ========================================================
    # Get All Categories
    # ========================================================

    @staticmethod
    def get_all_categories() -> list[Category]:
        """Get all active categories."""

        return CategoryRepository.get_all()

    # ========================================================
    # Update Category
    # ========================================================

    @staticmethod
    def update_category(
        category: Category
    ) -> bool:
        """Validate and update an existing category."""

        if category.category_id is None:

            raise ValueError(
                "Category ID is required."
            )

        CategoryService.validate_category(
            name=category.name,
            description=category.description
        )

        category.name = category.name.strip()

        category.description = (
            category.description.strip()
            if category.description
            else ""
        )

        return CategoryRepository.update(
            category
        )

    # ========================================================
    # Delete Category
    # ========================================================

    @staticmethod
    def delete_category(
        category_id: int
    ) -> bool:
        """Soft-delete an active category."""

        if category_id <= 0:

            raise ValueError(
                "Category ID must be greater than zero."
            )

        return CategoryRepository.delete(
            category_id
        )