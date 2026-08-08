from config.database import get_connection
from database.schema import initialize_database


EXPECTED_TABLES = {
    "users",
    "categories",
    "products",
    "cart",
    "orders",
    "order_items",
    "payments",
    "reviews",
}


def test_initialize_database():
    """
    Test that the database and all tables are created.
    """

    result = initialize_database()

    assert result is True


def test_all_tables_exist():
    """
    Test that all required PyCommerce tables exist.
    """

    connection = get_connection()

    assert connection is not None

    cursor = connection.cursor()

    cursor.execute("SHOW TABLES")

    tables = {row[0] for row in cursor.fetchall()}

    cursor.close()
    connection.close()

    assert EXPECTED_TABLES.issubset(tables)