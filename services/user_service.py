"""
user_service.py
---------------
Business logic related to users.
"""

from typing import Optional

from models.user import User
from repositories.user_repository import UserRepository
from services.auth_service import AuthService


class UserService:
    """Provides business operations for users."""

    # ========================================================
    # Validation
    # ========================================================

    @staticmethod
    def validate_username(username: str) -> None:
        """Validate a username/name."""

        if not username or not username.strip():
            raise ValueError(
                "Username cannot be empty."
            )

        if len(username.strip()) < 3:
            raise ValueError(
                "Username must contain at least 3 characters."
            )

    @staticmethod
    def validate_email(email: str) -> None:
        """Validate an email address."""

        if not email or not email.strip():
            raise ValueError(
                "Email cannot be empty."
            )

        if "@" not in email:
            raise ValueError(
                "Invalid email address."
            )

    @staticmethod
    def validate_password(password: str) -> None:
        """Validate a password."""

        if not password:
            raise ValueError(
                "Password cannot be empty."
            )

        if len(password) < 6:
            raise ValueError(
                "Password must contain at least 6 characters."
            )

    @staticmethod
    def validate_role(role: str) -> None:
        """Validate user role."""

        allowed_roles = {
            "customer",
            "admin"
        }

        if role not in allowed_roles:
            raise ValueError(
                "Role must be either 'customer' or 'admin'."
            )

    @staticmethod
    def validate_user(
        username: str,
        email: str,
        password: str,
        role: str = "customer"
    ) -> None:
        """Validate complete user information."""

        UserService.validate_username(username)
        UserService.validate_email(email)
        UserService.validate_password(password)
        UserService.validate_role(role)

    # ========================================================
    # Create User
    # ========================================================

    @staticmethod
    def create_user(
        user: User
    ) -> Optional[User]:
        """
        Validate and create a new user.

        The password is hashed before being stored.
        """

        UserService.validate_username(
            user.name
        )

        UserService.validate_email(
            user.email
        )

        UserService.validate_password(
            user.password
        )

        UserService.validate_role(
            user.role
        )

        user.name = user.name.strip()
        user.email = user.email.strip().lower()
        user.phone = user.phone.strip()
        user.address = user.address.strip()

        # Hash password before storing it.
        user.password = AuthService.hash_password(
            user.password
        )

        return UserRepository.create(user)

    # ========================================================
    # Get User
    # ========================================================

    @staticmethod
    def get_user(
        user_id: int
    ) -> Optional[User]:
        """Get an active user by ID."""

        if user_id <= 0:
            raise ValueError(
                "User ID must be greater than zero."
            )

        return UserRepository.get_by_id(
            user_id
        )

    @staticmethod
    def get_user_by_email(
        email: str
    ) -> Optional[User]:
        """Get an active user by email."""

        UserService.validate_email(email)

        return UserRepository.get_by_email(
            email.strip().lower()
        )

    @staticmethod
    def get_all_users() -> list[User]:
        """Get all active users."""

        return UserRepository.get_all()

    # ========================================================
    # Update User
    # ========================================================

    @staticmethod
    def update_user(
        user: User
    ) -> bool:
        """
        Validate and update an existing user.

        The password field is assumed to already contain
        the stored password hash.
        """

        if user.user_id is None:
            raise ValueError(
                "User ID is required."
            )

        UserService.validate_username(
            user.name
        )

        UserService.validate_email(
            user.email
        )

        UserService.validate_role(
            user.role
        )

        if not user.password:
            raise ValueError(
                "Password hash cannot be empty."
            )

        user.name = user.name.strip()
        user.email = user.email.strip().lower()
        user.phone = user.phone.strip()
        user.address = user.address.strip()

        return UserRepository.update(
            user
        )

    # ========================================================
    # Delete User
    # ========================================================

    @staticmethod
    def delete_user(
        user_id: int
    ) -> bool:
        """
        Soft-delete an active user.
        """

        if user_id <= 0:
            raise ValueError(
                "User ID must be greater than zero."
            )

        return UserRepository.delete(
            user_id
        )