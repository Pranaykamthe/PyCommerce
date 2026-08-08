"""
auth_service.py
---------------
Authentication and password management for PyCommerce.
"""

import hashlib
import re
from typing import Optional

from models.user import User
from repositories.user_repository import UserRepository


class AuthService:
    """Handles authentication and password operations."""

    # ========================================================
    # Password Hashing
    # ========================================================

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a password using SHA-256.

        Returns:
            str: Hexadecimal password hash.
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
        password_hash: str
    ) -> bool:
        """Verify a plain password against a stored hash."""

        if not password or not password_hash:
            return False

        hashed_password = (
            AuthService.hash_password(password)
        )

        return hashed_password == password_hash

    # ========================================================
    # Email Validation
    # ========================================================

    @staticmethod
    def validate_email(email: str) -> None:
        """Validate an email address."""

        if not email or not email.strip():
            raise ValueError(
                "Email cannot be empty."
            )

        pattern = (
            r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
        )

        if not re.match(pattern, email):
            raise ValueError(
                "Invalid email address."
            )

    # ========================================================
    # Password Validation
    # ========================================================

    @staticmethod
    def validate_password(
        password: str
    ) -> None:
        """Validate a password."""

        if not password:
            raise ValueError(
                "Password cannot be empty."
            )

        if len(password) < 6:
            raise ValueError(
                "Password must contain at least 6 characters."
            )

    # ========================================================
    # Registration
    # ========================================================

    @staticmethod
    def register(
        name: str,
        email: str,
        password: str,
        phone: str = "",
        address: str = ""
    ) -> Optional[User]:
        """
        Register a new customer.

        Password is hashed before being stored.
        """

        if not name or not name.strip():
            raise ValueError(
                "Name cannot be empty."
            )

        if len(name.strip()) < 3:
            raise ValueError(
                "Name must contain at least 3 characters."
            )

        AuthService.validate_email(
            email
        )

        AuthService.validate_password(
            password
        )

        email = email.strip().lower()

        # Check whether email already exists.
        existing_user = (
            UserRepository.get_by_email(email)
        )

        if existing_user is not None:
            raise ValueError(
                "Email is already registered."
            )

        hashed_password = (
            AuthService.hash_password(password)
        )

        user = User(
            name=name.strip(),
            email=email,
            password=hashed_password,
            phone=phone.strip(),
            address=address.strip(),
            role="customer"
        )

        return UserRepository.create(user)

    # ========================================================
    # Login
    # ========================================================

    @staticmethod
    def login(
        email: str,
        password: str
    ) -> Optional[User]:
        """
        Authenticate a user.

        Returns the User object if credentials are valid.
        Returns None if authentication fails.
        """

        AuthService.validate_email(
            email
        )

        if not password:
            raise ValueError(
                "Password cannot be empty."
            )

        email = email.strip().lower()

        user = UserRepository.get_by_email(
            email
        )

        if user is None:
            return None

        if not AuthService.verify_password(
            password,
            user.password
        ):
            return None

        return user

    # ========================================================
    # Admin Authentication
    # ========================================================

    @staticmethod
    def is_admin(
        user: Optional[User]
    ) -> bool:
        """Check whether a user is an administrator."""

        if user is None:
            return False

        return user.role == "admin"

    @staticmethod
    def is_customer(
        user: Optional[User]
    ) -> bool:
        """Check whether a user is a customer."""

        if user is None:
            return False

        return user.role == "customer"