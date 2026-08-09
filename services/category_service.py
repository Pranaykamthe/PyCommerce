"""
Business logic related to categories.
"""

from models.category import Category
from repositories.category_repository import CategoryRepository


class CategoryService:
    """Provides business operations for categories."""

    # ========================================================
    # Get All Categories
    # ========================================================

    @staticmethod
    def get_all_categories() -> list[Category]:
        """Get all active categories."""

        return CategoryRepository.get_all()