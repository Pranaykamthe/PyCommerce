"""
Pytest configuration for PyCommerce tests.
"""

from uuid import uuid4

import pytest

from config.database import get_connection, close_connection


@pytest.fixture
def unique_email():
    """Generate a unique email for tests."""
    return f"test_{uuid4().hex}@pycommerce.test"


@pytest.fixture(autouse=True)
def cleanup_payment_test_data():
    """
    Clean up payment test data after every test.

    Payment tests create:
        users
        orders
        order_items
        payments

    This fixture removes those records after each test.
    """

    yield

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        # Find test users created by payment tests.
        cursor.execute(
            """
            SELECT user_id
            FROM users
            WHERE email LIKE 'payment_test_%@gmail.com'
            """
        )

        user_ids = [row[0] for row in cursor.fetchall()]

        if not user_ids:
            return

        placeholders = ", ".join(["%s"] * len(user_ids))

        # Find orders belonging to test users.
        cursor.execute(
            f"""
            SELECT order_id
            FROM orders
            WHERE user_id IN ({placeholders})
            """,
            user_ids,
        )

        order_ids = [row[0] for row in cursor.fetchall()]

        if order_ids:
            order_placeholders = ", ".join(
                ["%s"] * len(order_ids)
            )

            # Delete payments first.
            cursor.execute(
                f"""
                DELETE FROM payments
                WHERE order_id IN ({order_placeholders})
                """,
                order_ids,
            )

            # Delete order items.
            cursor.execute(
                f"""
                DELETE FROM order_items
                WHERE order_id IN ({order_placeholders})
                """,
                order_ids,
            )

            # Delete orders.
            cursor.execute(
                f"""
                DELETE FROM orders
                WHERE order_id IN ({order_placeholders})
                """,
                order_ids,
            )

        # Delete carts.
        cursor.execute(
            f"""
            DELETE FROM cart
            WHERE user_id IN ({placeholders})
            """,
            user_ids,
        )

        # Delete reviews.
        cursor.execute(
            f"""
            DELETE FROM reviews
            WHERE user_id IN ({placeholders})
            """,
            user_ids,
        )

        # Delete test users.
        cursor.execute(
            f"""
            DELETE FROM users
            WHERE user_id IN ({placeholders})
            """,
            user_ids,
        )

        connection.commit()

    except Exception as exc:
        if connection:
            connection.rollback()

        print(f"\n[TEST CLEANUP WARNING] {exc}")

    finally:
        if cursor:
            cursor.close()

        if connection:
            close_connection(connection)