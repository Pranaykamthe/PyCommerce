"""
auth_service.py
---------------
Authentication and password-related business logic.
"""

import hashlib


class AuthService:
    """Provides authentication-related operations."""

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a password using SHA-256.

        Raises:
            ValueError: If the password is empty.
        """

        if not password:
            raise ValueError(
                "Password cannot be empty."
            )

        return hashlib.sha256(
            password.encode("utf-8")
        ).hexdigest()

    @staticmethod
    def verify_password(
        password: str,
        hashed_password: str
    ) -> bool:
        """
        Verify a password against a stored hash.
        """

        if not password or not hashed_password:
            return False

        password_hash = AuthService.hash_password(
            password
        )

        return password_hash == hashed_password