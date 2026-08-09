"""
Database operations for products.
"""

from typing import Optional

from config.database import (
    get_connection,
    close_connection
)

from models.product import Product


class ProductRepository:
    """Handles CRUD operations for products."""

    # ========================================================
    # Create Product
    # ========================================================

    @staticmethod
    def create(
        product: Product
    ) -> Optional[Product]:
        """Insert a new product into the database."""

        connection = get_connection()

        if connection is None:
            return None

        cursor = connection.cursor()

        try:

            query = """
                INSERT INTO products (
                    category_id,
                    product_name,
                    description,
                    price,
                    stock_quantity,
                    image_path
                )
                VALUES (%s, %s, %s, %s, %s, %s)
            """

            values = (
                product.category_id,
                product.name,
                product.description,
                product.price,
                product.stock,
                product.image_url
            )

            cursor.execute(
                query,
                values
            )

            connection.commit()

            product.product_id = cursor.lastrowid

            return product

        finally:

            cursor.close()
            close_connection(connection)

    # ========================================================
    # Get Product By ID
    # ========================================================

    @staticmethod
    def get_by_id(
        product_id: int
    ) -> Optional[Product]:
        """Get a product by its ID."""

        connection = get_connection()

        if connection is None:
            return None

        cursor = connection.cursor(
            dictionary=True
        )

        try:

            query = """
                SELECT
                    product_id,
                    category_id,
                    product_name,
                    description,
                    price,
                    stock_quantity,
                    image_path,
                    created_at,
                    updated_at
                FROM products
                WHERE product_id = %s
            """

            cursor.execute(
                query,
                (product_id,)
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return Product(
                product_id=row["product_id"],
                category_id=row["category_id"],
                name=row["product_name"],
                description=row["description"] or "",
                price=float(row["price"]),
                stock=row["stock_quantity"],
                image_url=row["image_path"] or "",
                created_at=str(row["created_at"]),
                updated_at=str(row["updated_at"])
            )

        finally:

            cursor.close()
            close_connection(connection)

    # ========================================================
    # Get All Products
    # ========================================================

    @staticmethod
    def get_all() -> list[Product]:
        """Return all products."""

        connection = get_connection()

        if connection is None:
            return []

        cursor = connection.cursor(
            dictionary=True
        )

        try:

            query = """
                SELECT
                    product_id,
                    category_id,
                    product_name,
                    description,
                    price,
                    stock_quantity,
                    image_path,
                    created_at,
                    updated_at
                FROM products
                ORDER BY product_id
            """

            cursor.execute(
                query
            )

            rows = cursor.fetchall()

            products = []

            for row in rows:

                product = Product(
                    product_id=row["product_id"],
                    category_id=row["category_id"],
                    name=row["product_name"],
                    description=row["description"] or "",
                    price=float(row["price"]),
                    stock=row["stock_quantity"],
                    image_url=row["image_path"] or "",
                    created_at=str(row["created_at"]),
                    updated_at=str(row["updated_at"])
                )

                products.append(product)

            return products

        finally:

            cursor.close()
            close_connection(connection)

    # ========================================================
    # Search Products By Name
    # ========================================================

    @staticmethod
    def search_by_name(
        search_term: str
    ) -> list[Product]:
        """
        Search products by product name.

        Uses a partial match.
        """

        connection = get_connection()

        if connection is None:
            return []

        cursor = connection.cursor(
            dictionary=True
        )

        try:

            query = """
                SELECT
                    product_id,
                    category_id,
                    product_name,
                    description,
                    price,
                    stock_quantity,
                    image_path,
                    created_at,
                    updated_at
                FROM products
                WHERE product_name LIKE %s
                ORDER BY product_id
            """

            values = (
                f"%{search_term}%",
            )

            cursor.execute(
                query,
                values
            )

            rows = cursor.fetchall()

            products = []

            for row in rows:

                product = Product(
                    product_id=row["product_id"],
                    category_id=row["category_id"],
                    name=row["product_name"],
                    description=row["description"] or "",
                    price=float(row["price"]),
                    stock=row["stock_quantity"],
                    image_url=row["image_path"] or "",
                    created_at=str(row["created_at"]),
                    updated_at=str(row["updated_at"])
                )

                products.append(product)

            return products

        finally:

            cursor.close()
            close_connection(connection)

    # ========================================================
    # Update Product
    # ========================================================

    @staticmethod
    def update(
        product: Product
    ) -> bool:
        """Update an existing product."""

        if product.product_id is None:
            return False

        connection = get_connection()

        if connection is None:
            return False

        cursor = connection.cursor()

        try:

            query = """
                UPDATE products
                SET
                    category_id = %s,
                    product_name = %s,
                    description = %s,
                    price = %s,
                    stock_quantity = %s,
                    image_path = %s
                WHERE product_id = %s
            """

            values = (
                product.category_id,
                product.name,
                product.description,
                product.price,
                product.stock,
                product.image_url,
                product.product_id
            )

            cursor.execute(
                query,
                values
            )

            connection.commit()

            return cursor.rowcount > 0

        finally:

            cursor.close()
            close_connection(connection)

    # ========================================================
    # Decrease Stock
    # ========================================================

    @staticmethod
    def decrease_stock(
        product_id: int,
        quantity: int
    ) -> bool:
        """
        Decrease product stock after a successful order.

        The update only happens when enough stock is available.

        Example:
            Current stock = 10
            Quantity sold = 2
            New stock = 8
        """

        if product_id <= 0:
            return False

        if quantity <= 0:
            return False

        connection = get_connection()

        if connection is None:
            return False

        cursor = connection.cursor()

        try:

            query = """
                UPDATE products
                SET stock_quantity = stock_quantity - %s
                WHERE product_id = %s
                  AND stock_quantity >= %s
            """

            values = (
                quantity,
                product_id,
                quantity
            )

            cursor.execute(
                query,
                values
            )

            connection.commit()

            return cursor.rowcount > 0

        finally:

            cursor.close()
            close_connection(connection)

    # ========================================================
    # Delete Product
    # ========================================================

    @staticmethod
    def delete(
        product_id: int
    ) -> bool:
        """Delete a product by its ID."""

        if product_id <= 0:
            return False

        connection = get_connection()

        if connection is None:
            return False

        cursor = connection.cursor()

        try:

            query = """
                DELETE FROM products
                WHERE product_id = %s
            """

            cursor.execute(
                query,
                (product_id,)
            )

            connection.commit()

            return cursor.rowcount > 0

        finally:

            cursor.close()
            close_connection(connection)