"""
user_service.py
---------------
Business logic related to users.
"""


class UserService:
    """Provides business operations for users."""

    @staticmethod
    def validate_username(username: str) -> None:
        """Validate a username."""

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
    def validate_user(
        username: str,
        email: str,
        password: str
    ) -> None:
        """Validate complete user information."""

        UserService.validate_username(username)
        UserService.validate_email(email)
        UserService.validate_password(password)