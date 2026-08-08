from config.database import (
    create_database,
    get_connection,
    close_connection
)


def test_create_database():
    """
    Test database creation.
    """

    create_database()

    connection = get_connection()

    assert connection is not None
    assert connection.is_connected()

    close_connection(connection)


def test_get_connection():
    """
    Test MySQL connection.
    """

    connection = get_connection()

    assert connection is not None
    assert connection.is_connected()

    close_connection(connection)