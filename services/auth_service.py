"""
Authentication and password management for PyCommerce.
"""

import hashlib
import hmac
import os
import re
from typing import Optional

from models.user import User
from repositories.user_repository import UserRepository


# ========================================================
# Password Security Configuration
# ========================================================

PASSWORD_ALGORITHM = "pbkdf2_sha256"
PASSWORD_ITERATIONS = 500_000
SALT_LENGTH = 16
HASH_LENGTH = 32


class AuthService:
    """Handles authentication and password operations."""

    # ========================================================
    # Password Hashing
    # ========================================================

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a password using PBKDF2-HMAC-SHA256.

        A random salt is generated for every password.

        Returns:
            str: Encoded password hash containing:
                algorithm,
                iterations,
                salt,
                and derived key.
        """

        if not password:
            raise ValueError(
                "Password cannot be empty."
            )

        salt = os.urandom(
            SALT_LENGTH
        )

        derived_key = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            PASSWORD_ITERATIONS,
            dklen=HASH_LENGTH
        )

        return (
            f"{PASSWORD_ALGORITHM}$"
            f"{PASSWORD_ITERATIONS}$"
            f"{salt.hex()}$"
            f"{derived_key.hex()}"
        )

    @staticmethod
    def verify_password(
        password: str,
        password_hash: str
    ) -> bool:
        """
        Verify a password against a stored hash.

        Supports:
        - PBKDF2-HMAC-SHA256 hashes
        - Legacy SHA-256 hashes

        Returns:
            bool: True if the password is valid,
            otherwise False.
        """

        if not password or not password_hash:
            return False

        # ====================================================
        # New PBKDF2-SHA256 Format
        # ====================================================

        if password_hash.startswith(
            f"{PASSWORD_ALGORITHM}$"
        ):

            try:
                (
                    algorithm,
                    iterations,
                    salt_hex,
                    stored_hash
                ) = password_hash.split("$")

                if algorithm != PASSWORD_ALGORITHM:
                    return False

                salt = bytes.fromhex(
                    salt_hex
                )

                derived_key = hashlib.pbkdf2_hmac(
                    "sha256",
                    password.encode("utf-8"),
                    salt,
                    int(iterations),
                    dklen=HASH_LENGTH
                )

                return hmac.compare_digest(
                    derived_key.hex(),
                    stored_hash
                )

            except (
                ValueError,
                TypeError
            ):
                return False

        # ====================================================
        # Legacy SHA-256 Compatibility
        # ====================================================

        if len(password_hash) == 64:

            legacy_hash = hashlib.sha256(
                password.encode("utf-8")
            ).hexdigest()

            return hmac.compare_digest(
                legacy_hash,
                password_hash
            )

        return False

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

        Returns:
            User object if credentials are valid.
            None if authentication fails.

        Legacy SHA-256 passwords are automatically upgraded
        to PBKDF2 after successful authentication.
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

        # ====================================================
        # Upgrade Legacy SHA-256 Password
        # ====================================================

        if len(user.password) == 64:

            user.password = (
                AuthService.hash_password(
                    password
                )
            )

            UserRepository.update(
                user
            )

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

    # ========================================================
    # Customer Authentication
    # ========================================================

    @staticmethod
    def is_customer(
        user: Optional[User]
    ) -> bool:
        """Check whether a user is a customer."""

        if user is None:
            return False

        return user.role == "customer"