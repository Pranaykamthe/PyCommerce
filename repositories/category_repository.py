"""
Database operations for categories.
"""

from config.database import (
    get_connection,
    close_connection
)

from models.category import Category


class CategoryRepository:
    """Handles database operations for categories."""

    # ========================================================
    # Get All Active Categories
    # ========================================================

    @staticmethod
    def get_all() -> list[Category]:
        """Return all active categories."""

        connection = get_connection()

        if connection is None:
            return []

        cursor = connection.cursor(
            dictionary=True
        )

        try:

            query = """
                SELECT
                    category_id,
                    category_name,
                    description,
                    created_at
                FROM categories
                WHERE is_active = 1
                ORDER BY category_id
            """

            cursor.execute(query)

            rows = cursor.fetchall()

            categories = []

            for row in rows:

                category = Category(
                    category_id=row["category_id"],
                    name=row["category_name"],
                    description=row["description"] or "",
                    created_at=str(row["created_at"])
                )

                categories.append(category)

            return categories

        finally:

            cursor.close()
            close_connection(connection)