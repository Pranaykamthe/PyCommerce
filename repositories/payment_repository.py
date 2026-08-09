"""
Database operations for payments.
"""

from typing import Optional

from config.database import (
    get_connection,
    close_connection
)

from models.payment import Payment


class PaymentRepository:
    """Handles CRUD operations for payments."""

    # ========================================================
    # Create Payment
    # ========================================================

    @staticmethod
    def create(
        payment: Payment
    ) -> Optional[Payment]:
        """
        Insert a new payment into the database.

        Returns:
            Created Payment object or None if
            database connection fails.
        """

        connection = get_connection()

        if connection is None:
            return None

        cursor = connection.cursor()

        try:
            query = """
                INSERT INTO payments (
                    order_id,
                    payment_method,
                    payment_status,
                    transaction_id,
                    amount
                )
                VALUES (%s, %s, %s, %s, %s)
            """

            values = (
                payment.order_id,
                payment.payment_method,
                payment.status,
                payment.transaction_id,
                payment.amount
            )

            cursor.execute(
                query,
                values
            )

            connection.commit()

            payment.payment_id = cursor.lastrowid

            return payment

        finally:
            cursor.close()
            close_connection(connection)

    # ========================================================
    # Get Payment By ID
    # ========================================================

    @staticmethod
    def get_by_id(
        payment_id: int
    ) -> Optional[Payment]:
        """
        Get a payment by payment ID.
        """

        connection = get_connection()

        if connection is None:
            return None

        cursor = connection.cursor(
            dictionary=True
        )

        try:
            query = """
                SELECT
                    payment_id,
                    order_id,
                    payment_method,
                    payment_status,
                    transaction_id,
                    amount,
                    payment_date
                FROM payments
                WHERE payment_id = %s
            """

            cursor.execute(
                query,
                (payment_id,)
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return Payment(
                payment_id=row["payment_id"],
                order_id=row["order_id"],
                payment_method=row["payment_method"],
                transaction_id=row["transaction_id"],
                amount=float(row["amount"]),
                status=row["payment_status"],
                paid_at=str(row["payment_date"])
            )

        finally:
            cursor.close()
            close_connection(connection)

    # ========================================================
    # Get Payment By Order
    # ========================================================

    @staticmethod
    def get_by_order_id(
        order_id: int
    ) -> Optional[Payment]:
        """
        Get the payment associated with an order.
        """

        connection = get_connection()

        if connection is None:
            return None

        cursor = connection.cursor(
            dictionary=True
        )

        try:
            query = """
                SELECT
                    payment_id,
                    order_id,
                    payment_method,
                    payment_status,
                    transaction_id,
                    amount,
                    payment_date
                FROM payments
                WHERE order_id = %s
                LIMIT 1
            """

            cursor.execute(
                query,
                (order_id,)
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return Payment(
                payment_id=row["payment_id"],
                order_id=row["order_id"],
                payment_method=row["payment_method"],
                transaction_id=row["transaction_id"],
                amount=float(row["amount"]),
                status=row["payment_status"],
                paid_at=str(row["payment_date"])
            )

        finally:
            cursor.close()
            close_connection(connection)

    # ========================================================
    # Get All Payments
    # ========================================================

    @staticmethod
    def get_all() -> list[Payment]:
        """
        Return all payments.
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
                    payment_id,
                    order_id,
                    payment_method,
                    payment_status,
                    transaction_id,
                    amount,
                    payment_date
                FROM payments
                ORDER BY payment_id
            """

            cursor.execute(query)

            rows = cursor.fetchall()

            payments = []

            for row in rows:
                payment = Payment(
                    payment_id=row["payment_id"],
                    order_id=row["order_id"],
                    payment_method=row[
                        "payment_method"
                    ],
                    transaction_id=row[
                        "transaction_id"
                    ],
                    amount=float(
                        row["amount"]
                    ),
                    status=row[
                        "payment_status"
                    ],
                    paid_at=str(
                        row["payment_date"]
                    )
                )

                payments.append(payment)

            return payments

        finally:
            cursor.close()
            close_connection(connection)

    # ========================================================
    # Update Payment
    # ========================================================

    @staticmethod
    def update(
        payment: Payment
    ) -> bool:
        """
        Update an existing payment.
        """

        if payment.payment_id is None:
            return False

        connection = get_connection()

        if connection is None:
            return False

        cursor = connection.cursor()

        try:
            query = """
                UPDATE payments
                SET
                    payment_method = %s,
                    payment_status = %s,
                    transaction_id = %s,
                    amount = %s
                WHERE payment_id = %s
            """

            values = (
                payment.payment_method,
                payment.status,
                payment.transaction_id,
                payment.amount,
                payment.payment_id
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
    # Delete Payment
    # ========================================================

    @staticmethod
    def delete(
        payment_id: int
    ) -> bool:
        """
        Delete a payment by ID.
        """

        connection = get_connection()

        if connection is None:
            return False

        cursor = connection.cursor()

        try:
            query = """
                DELETE FROM payments
                WHERE payment_id = %s
            """

            cursor.execute(
                query,
                (payment_id,)
            )

            connection.commit()

            return cursor.rowcount > 0

        finally:
            cursor.close()
            close_connection(connection)