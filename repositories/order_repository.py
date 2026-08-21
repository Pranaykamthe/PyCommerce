"""
order_repository.py
-------------------
Database operations for orders and order items.
"""

from typing import Optional

from config.database import get_connection, close_connection
from models.order import Order
from models.order_item import OrderItem


class OrderRepository:
    """Handles database operations for orders."""

    # ========================================================
    # Order Operations
    # ========================================================

    @staticmethod
    def create_order(
        order: Order
    ) -> Optional[Order]:
        """Create a new order."""

        connection = get_connection()

        if connection is None:
            return None

        cursor = connection.cursor()

        try:
            query = """
                INSERT INTO orders (
                    user_id,
                    total_amount,
                    order_status,
                    shipping_address
                )
                VALUES (%s, %s, %s, %s)
            """

            values = (
                order.user_id,
                order.total_amount,
                order.status,
                order.shipping_address
            )

            cursor.execute(query, values)
            connection.commit()

            order.order_id = cursor.lastrowid

            return order

        finally:
            cursor.close()
            close_connection(connection)

    @staticmethod
    def get_order_by_id(
        order_id: int
    ) -> Optional[Order]:
        """Get an order by ID."""

        connection = get_connection()

        if connection is None:
            return None

        cursor = connection.cursor(dictionary=True)

        try:
            query = """
                SELECT
                    order_id,
                    user_id,
                    total_amount,
                    order_status,
                    shipping_address,
                    order_date,
                    updated_at
                FROM orders
                WHERE order_id = %s
            """

            cursor.execute(
                query,
                (order_id,)
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return Order(
                order_id=row["order_id"],
                user_id=row["user_id"],
                total_amount=float(row["total_amount"]),
                status=row["order_status"],
                shipping_address=row["shipping_address"],
                created_at=str(row["order_date"]),
                updated_at=str(row["updated_at"])
            )

        finally:
            cursor.close()
            close_connection(connection)

    @staticmethod
    def get_orders_by_user(
        user_id: int
    ) -> list[Order]:
        """Get all orders belonging to a user."""

        connection = get_connection()

        if connection is None:
            return []

        cursor = connection.cursor(dictionary=True)

        try:
            query = """
                SELECT
                    order_id,
                    user_id,
                    total_amount,
                    order_status,
                    shipping_address,
                    order_date,
                    updated_at
                FROM orders
                WHERE user_id = %s
                ORDER BY order_id DESC
            """

            cursor.execute(
                query,
                (user_id,)
            )

            rows = cursor.fetchall()

            orders = []

            for row in rows:
                order = Order(
                    order_id=row["order_id"],
                    user_id=row["user_id"],
                    total_amount=float(row["total_amount"]),
                    status=row["order_status"],
                    shipping_address=row["shipping_address"],
                    created_at=str(row["order_date"]),
                    updated_at=str(row["updated_at"])
                )

                orders.append(order)

            return orders

        finally:
            cursor.close()
            close_connection(connection)

    @staticmethod
    def update_order(
        order: Order
    ) -> bool:
        """Update an existing order."""

        if order.order_id is None:
            return False

        connection = get_connection()

        if connection is None:
            return False

        cursor = connection.cursor()

        try:
            query = """
                UPDATE orders
                SET
                    total_amount = %s,
                    order_status = %s,
                    shipping_address = %s
                WHERE order_id = %s
            """

            values = (
                order.total_amount,
                order.status,
                order.shipping_address,
                order.order_id
            )

            cursor.execute(query, values)
            connection.commit()

            return cursor.rowcount > 0

        finally:
            cursor.close()
            close_connection(connection)

    @staticmethod
    def delete_order(
        order_id: int
    ) -> bool:
        """
        Delete an order and its order items.

        Order items are deleted first because they reference
        the order.
        """

        connection = get_connection()

        if connection is None:
            return False

        cursor = connection.cursor()

        try:
            delete_items_query = """
                DELETE FROM order_items
                WHERE order_id = %s
            """

            cursor.execute(
                delete_items_query,
                (order_id,)
            )

            delete_order_query = """
                DELETE FROM orders
                WHERE order_id = %s
            """

            cursor.execute(
                delete_order_query,
                (order_id,)
            )

            connection.commit()

            return cursor.rowcount > 0

        finally:
            cursor.close()
            close_connection(connection)

    # ========================================================
    # Order Item Operations
    # ========================================================

    @staticmethod
    def create_order_item(
        order_item: OrderItem
    ) -> Optional[OrderItem]:
        """Create a new order item."""

        connection = get_connection()

        if connection is None:
            return None

        cursor = connection.cursor()

        try:
            subtotal = (
                order_item.quantity *
                order_item.price
            )

            query = """
                INSERT INTO order_items (
                    order_id,
                    product_id,
                    quantity,
                    unit_price,
                    subtotal
                )
                VALUES (%s, %s, %s, %s, %s)
            """

            values = (
                order_item.order_id,
                order_item.product_id,
                order_item.quantity,
                order_item.price,
                subtotal
            )

            cursor.execute(query, values)
            connection.commit()

            order_item.order_item_id = (
                cursor.lastrowid
            )

            # Keep the model synchronized with
            # the value stored in the database.
            order_item.subtotal = subtotal

            return order_item

        finally:
            cursor.close()
            close_connection(connection)

    @staticmethod
    def get_order_item_by_id(
        order_item_id: int
    ) -> Optional[OrderItem]:
        """Get an order item by ID."""

        connection = get_connection()

        if connection is None:
            return None

        cursor = connection.cursor(dictionary=True)

        try:
            query = """
                SELECT
                    order_item_id,
                    order_id,
                    product_id,
                    quantity,
                    unit_price,
                    subtotal
                FROM order_items
                WHERE order_item_id = %s
            """

            cursor.execute(
                query,
                (order_item_id,)
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return OrderItem(
                order_item_id=row["order_item_id"],
                order_id=row["order_id"],
                product_id=row["product_id"],
                quantity=row["quantity"],
                price=float(row["unit_price"]),
                subtotal=float(row["subtotal"])
            )

        finally:
            cursor.close()
            close_connection(connection)

    @staticmethod
    def get_order_items(
        order_id: int
    ) -> list[OrderItem]:
        """Get all items belonging to an order."""

        connection = get_connection()

        if connection is None:
            return []

        cursor = connection.cursor(dictionary=True)

        try:
            query = """
                SELECT
                    order_item_id,
                    order_id,
                    product_id,
                    quantity,
                    unit_price,
                    subtotal
                FROM order_items
                WHERE order_id = %s
                ORDER BY order_item_id
            """

            cursor.execute(
                query,
                (order_id,)
            )

            rows = cursor.fetchall()

            items = []

            for row in rows:
                item = OrderItem(
                    order_item_id=row["order_item_id"],
                    order_id=row["order_id"],
                    product_id=row["product_id"],
                    quantity=row["quantity"],
                    price=float(row["unit_price"]),
                    subtotal=float(row["subtotal"])
                )

                items.append(item)

            return items

        finally:
            cursor.close()
            close_connection(connection)

    @staticmethod
    def update_order_item(
        order_item: OrderItem
    ) -> bool:
        """Update an existing order item."""

        if order_item.order_item_id is None:
            return False

        connection = get_connection()

        if connection is None:
            return False

        cursor = connection.cursor()

        try:
            subtotal = (
                order_item.quantity *
                order_item.price
            )

            query = """
                UPDATE order_items
                SET
                    product_id = %s,
                    quantity = %s,
                    unit_price = %s,
                    subtotal = %s
                WHERE order_item_id = %s
            """

            values = (
                order_item.product_id,
                order_item.quantity,
                order_item.price,
                subtotal,
                order_item.order_item_id
            )

            cursor.execute(query, values)
            connection.commit()

            # Keep the model synchronized.
            order_item.subtotal = subtotal

            return cursor.rowcount > 0

        finally:
            cursor.close()
            close_connection(connection)

    @staticmethod
    def delete_order_item(
        order_item_id: int
    ) -> bool:
        """Delete an order item."""

        connection = get_connection()

        if connection is None:
            return False

        cursor = connection.cursor()

        try:
            query = """
                DELETE FROM order_items
                WHERE order_item_id = %s
            """

            cursor.execute(
                query,
                (order_item_id,)
            )

            connection.commit()

            return cursor.rowcount > 0

        finally:
            cursor.close()
            close_connection(connection)