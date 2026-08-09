"""
Database operations for wishlist.
"""

from typing import Optional

from config.database import (
    get_connection,
    close_connection
)

from models.wishlist import Wishlist


class WishlistRepository:
    """Handles CRUD operations for wishlist."""

    # ========================================================
    # Create
    # ========================================================

    @staticmethod
    def create(
        wishlist: Wishlist
    ) -> Optional[Wishlist]:
        """Insert a new wishlist item."""

        connection = get_connection()

        if connection is None:
            return None

        cursor = connection.cursor()

        try:
            query = """
                INSERT INTO wishlist (
                    user_id,
                    product_id
                )
                VALUES (%s, %s)
            """

            values = (
                wishlist.user_id,
                wishlist.product_id
            )

            cursor.execute(
                query,
                values
            )

            connection.commit()

            wishlist.wishlist_id = cursor.lastrowid

            return wishlist

        finally:
            cursor.close()
            close_connection(connection)

    # ========================================================
    # Get By ID
    # ========================================================

    @staticmethod
    def get_by_id(
        wishlist_id: int
    ) -> Optional[Wishlist]:
        """Get a wishlist item by its ID."""

        connection = get_connection()

        if connection is None:
            return None

        cursor = connection.cursor(
            dictionary=True
        )

        try:
            query = """
                SELECT
                    wishlist_id,
                    user_id,
                    product_id,
                    added_at
                FROM wishlist
                WHERE wishlist_id = %s
            """

            cursor.execute(
                query,
                (wishlist_id,)
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return Wishlist(
                wishlist_id=row["wishlist_id"],
                user_id=row["user_id"],
                product_id=row["product_id"],
                added_at=row["added_at"]
            )

        finally:
            cursor.close()
            close_connection(connection)

    # ========================================================
    # Get By User + Product
    # ========================================================

    @staticmethod
    def get_by_user_and_product(
        user_id: int,
        product_id: int
    ) -> Optional[Wishlist]:
        """Get a specific product from a user's wishlist."""

        connection = get_connection()

        if connection is None:
            return None

        cursor = connection.cursor(
            dictionary=True
        )

        try:
            query = """
                SELECT
                    wishlist_id,
                    user_id,
                    product_id,
                    added_at
                FROM wishlist
                WHERE user_id = %s
                  AND product_id = %s
            """

            cursor.execute(
                query,
                (
                    user_id,
                    product_id
                )
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return Wishlist(
                wishlist_id=row["wishlist_id"],
                user_id=row["user_id"],
                product_id=row["product_id"],
                added_at=row["added_at"]
            )

        finally:
            cursor.close()
            close_connection(connection)

    # ========================================================
    # Get By User
    # ========================================================

    @staticmethod
    def get_by_user(
        user_id: int
    ) -> list[Wishlist]:
        """Get all wishlist items belonging to a user."""

        connection = get_connection()

        if connection is None:
            return []

        cursor = connection.cursor(
            dictionary=True
        )

        try:
            query = """
                SELECT
                    wishlist_id,
                    user_id,
                    product_id,
                    added_at
                FROM wishlist
                WHERE user_id = %s
                ORDER BY wishlist_id
            """

            cursor.execute(
                query,
                (user_id,)
            )

            rows = cursor.fetchall()

            wishlists = []

            for row in rows:
                wishlist = Wishlist(
                    wishlist_id=row["wishlist_id"],
                    user_id=row["user_id"],
                    product_id=row["product_id"],
                    added_at=row["added_at"]
                )

                wishlists.append(wishlist)

            return wishlists

        finally:
            cursor.close()
            close_connection(connection)

    # ========================================================
    # Delete
    # ========================================================

    @staticmethod
    def delete(
        wishlist_id: int
    ) -> bool:
        """Delete a wishlist item."""

        connection = get_connection()

        if connection is None:
            return False

        cursor = connection.cursor()

        try:
            query = """
                DELETE FROM wishlist
                WHERE wishlist_id = %s
            """

            cursor.execute(
                query,
                (wishlist_id,)
            )

            connection.commit()

            return cursor.rowcount > 0

        finally:
            cursor.close()
            close_connection(connection)

    # ========================================================
    # Clear User Wishlist
    # ========================================================

    @staticmethod
    def clear_user_wishlist(
        user_id: int
    ) -> bool:
        """Delete all wishlist items belonging to a user."""

        connection = get_connection()

        if connection is None:
            return False

        cursor = connection.cursor()

        try:
            query = """
                DELETE FROM wishlist
                WHERE user_id = %s
            """

            cursor.execute(
                query,
                (user_id,)
            )

            connection.commit()

            return cursor.rowcount > 0

        finally:
            cursor.close()
            close_connection(connection)