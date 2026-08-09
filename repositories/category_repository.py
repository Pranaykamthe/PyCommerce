"""
Database operations for categories.
"""

from typing import Optional

from config.database import (
    get_connection,
    close_connection
)

from models.category import Category


class CategoryRepository:
    """Handles database operations for categories."""

    # ========================================================
    # Create Category
    # ========================================================

    @staticmethod
    def create(
        category: Category
    ) -> Optional[Category]:
        """Create a new category."""

        connection = get_connection()

        if connection is None:
            return None

        cursor = connection.cursor()

        try:

            query = """
                INSERT INTO categories (
                    category_name,
                    description
                )
                VALUES (%s, %s)
            """

            cursor.execute(
                query,
                (
                    category.name,
                    category.description
                )
            )

            connection.commit()

            category.category_id = (
                cursor.lastrowid
            )

            return category

        finally:

            cursor.close()
            close_connection(connection)

    # ========================================================
    # Get Category By ID
    # ========================================================

    @staticmethod
    def get_by_id(
        category_id: int
    ) -> Optional[Category]:
        """Return an active category by ID."""

        connection = get_connection()

        if connection is None:
            return None

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
                WHERE category_id = %s
                  AND is_active = 1
            """

            cursor.execute(
                query,
                (category_id,)
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return Category(
                category_id=row["category_id"],
                name=row["category_name"],
                description=row["description"] or "",
                created_at=str(
                    row["created_at"]
                )
            )

        finally:

            cursor.close()
            close_connection(connection)

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
                    created_at=str(
                        row["created_at"]
                    )
                )

                categories.append(
                    category
                )

            return categories

        finally:

            cursor.close()
            close_connection(connection)

    # ========================================================
    # Update Category
    # ========================================================

    @staticmethod
    def update(
        category: Category
    ) -> bool:
        """Update an existing active category."""

        if category.category_id is None:
            return False

        connection = get_connection()

        if connection is None:
            return False

        cursor = connection.cursor()

        try:

            query = """
                UPDATE categories
                SET
                    category_name = %s,
                    description = %s
                WHERE category_id = %s
                  AND is_active = 1
            """

            cursor.execute(
                query,
                (
                    category.name,
                    category.description,
                    category.category_id
                )
            )

            connection.commit()

            return cursor.rowcount > 0

        finally:

            cursor.close()
            close_connection(connection)

    # ========================================================
    # Delete Category
    # ========================================================

    @staticmethod
    def delete(
        category_id: int
    ) -> bool:
        """
        Soft-delete an active category.

        The category remains in the database but is
        marked as inactive.
        """

        connection = get_connection()

        if connection is None:
            return False

        cursor = connection.cursor()

        try:

            query = """
                UPDATE categories
                SET is_active = 0
                WHERE category_id = %s
                  AND is_active = 1
            """

            cursor.execute(
                query,
                (category_id,)
            )

            connection.commit()

            return cursor.rowcount > 0

        finally:

            cursor.close()
            close_connection(connection)