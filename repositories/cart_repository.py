"""
Database operations for shopping cart.
"""

from typing import Optional

from config.database import (
    get_connection,
    close_connection
)

from models.cart import Cart


class CartRepository:
    """Handles CRUD operations for shopping cart."""

    # ========================================================
    # Create
    # ========================================================

    @staticmethod
    def create(
        cart: Cart
    ) -> Optional[Cart]:
        """Insert a new cart item."""

        connection = get_connection()

        if connection is None:
            return None

        cursor = connection.cursor()

        try:
            query = """
                INSERT INTO cart (
                    user_id,
                    product_id,
                    quantity
                )
                VALUES (%s, %s, %s)
            """

            values = (
                cart.user_id,
                cart.product_id,
                cart.quantity
            )

            cursor.execute(
                query,
                values
            )

            connection.commit()

            cart.cart_id = cursor.lastrowid

            return cart

        finally:
            cursor.close()
            close_connection(connection)

    # ========================================================
    # Get By ID
    # ========================================================

    @staticmethod
    def get_by_id(
        cart_id: int
    ) -> Optional[Cart]:
        """Get a cart item by its ID."""

        connection = get_connection()

        if connection is None:
            return None

        cursor = connection.cursor(
            dictionary=True
        )

        try:
            query = """
                SELECT
                    c.cart_id,
                    c.user_id,
                    c.product_id,
                    p.product_name,
                    c.quantity,
                    p.price
                FROM cart c
                INNER JOIN products p
                    ON c.product_id = p.product_id
                WHERE c.cart_id = %s
            """

            cursor.execute(
                query,
                (cart_id,)
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return Cart(
                cart_id=row["cart_id"],
                user_id=row["user_id"],
                product_id=row["product_id"],
                product_name=row["product_name"],
                quantity=row["quantity"],
                price=float(row["price"])
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
    ) -> Optional[Cart]:
        """Get a user's cart item for a specific product."""

        connection = get_connection()

        if connection is None:
            return None

        cursor = connection.cursor(
            dictionary=True
        )

        try:
            query = """
                SELECT
                    c.cart_id,
                    c.user_id,
                    c.product_id,
                    p.product_name,
                    c.quantity,
                    p.price
                FROM cart c
                INNER JOIN products p
                    ON c.product_id = p.product_id
                WHERE c.user_id = %s
                  AND c.product_id = %s
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

            return Cart(
                cart_id=row["cart_id"],
                user_id=row["user_id"],
                product_id=row["product_id"],
                product_name=row["product_name"],
                quantity=row["quantity"],
                price=float(row["price"])
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
    ) -> list[Cart]:
        """Get all cart items belonging to a user."""

        connection = get_connection()

        if connection is None:
            return []

        cursor = connection.cursor(
            dictionary=True
        )

        try:
            query = """
                SELECT
                    c.cart_id,
                    c.user_id,
                    c.product_id,
                    p.product_name,
                    c.quantity,
                    p.price
                FROM cart c
                INNER JOIN products p
                    ON c.product_id = p.product_id
                WHERE c.user_id = %s
                ORDER BY c.cart_id
            """

            cursor.execute(
                query,
                (user_id,)
            )

            rows = cursor.fetchall()

            carts = []

            for row in rows:
                cart = Cart(
                    cart_id=row["cart_id"],
                    user_id=row["user_id"],
                    product_id=row["product_id"],
                    product_name=row["product_name"],
                    quantity=row["quantity"],
                    price=float(row["price"])
                )

                carts.append(cart)

            return carts

        finally:
            cursor.close()
            close_connection(connection)

    # ========================================================
    # Update Quantity
    # ========================================================

    @staticmethod
    def update_quantity(
        cart_id: int,
        quantity: int
    ) -> bool:
        """Update the quantity of a cart item."""

        connection = get_connection()

        if connection is None:
            return False

        cursor = connection.cursor()

        try:
            query = """
                UPDATE cart
                SET quantity = %s
                WHERE cart_id = %s
            """

            cursor.execute(
                query,
                (
                    quantity,
                    cart_id
                )
            )

            connection.commit()

            return cursor.rowcount > 0

        finally:
            cursor.close()
            close_connection(connection)

    # ========================================================
    # Delete
    # ========================================================

    @staticmethod
    def delete(
        cart_id: int
    ) -> bool:
        """Delete a cart item."""

        connection = get_connection()

        if connection is None:
            return False

        cursor = connection.cursor()

        try:
            query = """
                DELETE FROM cart
                WHERE cart_id = %s
            """

            cursor.execute(
                query,
                (cart_id,)
            )

            connection.commit()

            return cursor.rowcount > 0

        finally:
            cursor.close()
            close_connection(connection)

    # ========================================================
    # Clear User Cart
    # ========================================================

    @staticmethod
    def clear_user_cart(
        user_id: int
    ) -> bool:
        """Delete all cart items belonging to a user."""

        connection = get_connection()

        if connection is None:
            return False

        cursor = connection.cursor()

        try:
            query = """
                DELETE FROM cart
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