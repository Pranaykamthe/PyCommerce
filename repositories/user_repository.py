"""
user_repository.py
------------------
Database operations for users.
"""

from typing import Optional

from config.database import get_connection, close_connection
from models.user import User


class UserRepository:
    """Handles CRUD operations for users."""

    @staticmethod
    def create(user: User) -> Optional[User]:
        """
        Insert a new user into the database.

        The password must already be hashed before
        calling this method.
        """

        connection = get_connection()

        if connection is None:
            return None

        cursor = connection.cursor()

        try:
            query = """
                INSERT INTO users (
                    name,
                    email,
                    password_hash,
                    phone,
                    address,
                    role
                )
                VALUES (%s, %s, %s, %s, %s, %s)
            """

            values = (
                user.name,
                user.email,
                user.password,
                user.phone,
                user.address,
                user.role
            )

            cursor.execute(query, values)
            connection.commit()

            user.user_id = cursor.lastrowid

            return user

        finally:
            cursor.close()
            close_connection(connection)

    @staticmethod
    def get_by_id(
        user_id: int
    ) -> Optional[User]:
        """Get a user by ID."""

        connection = get_connection()

        if connection is None:
            return None

        cursor = connection.cursor(dictionary=True)

        try:
            query = """
                SELECT
                    user_id,
                    name,
                    email,
                    password_hash,
                    phone,
                    address,
                    role,
                    created_at
                FROM users
                WHERE user_id = %s
                  AND is_active = 1
            """

            cursor.execute(
                query,
                (user_id,)
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return User(
                user_id=row["user_id"],
                name=row["name"],
                email=row["email"],
                password=row["password_hash"],
                phone=row["phone"] or "",
                address=row["address"] or "",
                role=row["role"],
                created_at=str(row["created_at"])
            )

        finally:
            cursor.close()
            close_connection(connection)

    @staticmethod
    def get_by_email(
        email: str
    ) -> Optional[User]:
        """Get an active user by email."""

        connection = get_connection()

        if connection is None:
            return None

        cursor = connection.cursor(dictionary=True)

        try:
            query = """
                SELECT
                    user_id,
                    name,
                    email,
                    password_hash,
                    phone,
                    address,
                    role,
                    created_at
                FROM users
                WHERE email = %s
                  AND is_active = 1
            """

            cursor.execute(
                query,
                (email,)
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return User(
                user_id=row["user_id"],
                name=row["name"],
                email=row["email"],
                password=row["password_hash"],
                phone=row["phone"] or "",
                address=row["address"] or "",
                role=row["role"],
                created_at=str(row["created_at"])
            )

        finally:
            cursor.close()
            close_connection(connection)

    @staticmethod
    def get_all() -> list[User]:
        """Return all active users."""

        connection = get_connection()

        if connection is None:
            return []

        cursor = connection.cursor(dictionary=True)

        try:
            query = """
                SELECT
                    user_id,
                    name,
                    email,
                    password_hash,
                    phone,
                    address,
                    role,
                    created_at
                FROM users
                WHERE is_active = 1
                ORDER BY user_id
            """

            cursor.execute(query)

            rows = cursor.fetchall()

            users = []

            for row in rows:
                user = User(
                    user_id=row["user_id"],
                    name=row["name"],
                    email=row["email"],
                    password=row["password_hash"],
                    phone=row["phone"] or "",
                    address=row["address"] or "",
                    role=row["role"],
                    created_at=str(row["created_at"])
                )

                users.append(user)

            return users

        finally:
            cursor.close()
            close_connection(connection)

    @staticmethod
    def update(user: User) -> bool:
        """Update an existing user."""

        if user.user_id is None:
            return False

        connection = get_connection()

        if connection is None:
            return False

        cursor = connection.cursor()

        try:
            query = """
                UPDATE users
                SET
                    name = %s,
                    email = %s,
                    password_hash = %s,
                    phone = %s,
                    address = %s,
                    role = %s
                WHERE user_id = %s
            """

            values = (
                user.name,
                user.email,
                user.password,
                user.phone,
                user.address,
                user.role,
                user.user_id
            )

            cursor.execute(query, values)
            connection.commit()

            return cursor.rowcount > 0

        finally:
            cursor.close()
            close_connection(connection)

    @staticmethod
    def delete(user_id: int) -> bool:
        """
        Deactivate a user.

        We use a soft delete instead of physically
        deleting the user from the database.
        """

        connection = get_connection()

        if connection is None:
            return False

        cursor = connection.cursor()

        try:
            query = """
                UPDATE users
                SET
                    is_active = 0
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