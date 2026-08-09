"""
auth_ui.py
---------
Authentication user interface for PyCommerce.
"""

from typing import Optional

from models.user import User

from services.auth_service import AuthService
from services.user_service import UserService

from utils.console import console
from utils.input_helper import get_text

from utils.messages import (
    success,
    error,
)


# ============================================================
# Customer Registration
# ============================================================

def register_user() -> Optional[User]:
    """
    Display customer registration form and register a new customer.

    Returns:
        User object if registration succeeds,
        otherwise None.
    """

    console.print(
        "\n[bold cyan]=== Customer Registration ===[/bold cyan]\n"
    )

    try:

        name = get_text(
            "Enter name: "
        )

        email = get_text(
            "Enter email: "
        )

        password = get_text(
            "Enter password: "
        )

        phone = get_text(
            "Enter phone: "
        )

        address = get_text(
            "Enter address: "
        )

        user = AuthService.register(
            name=name,
            email=email,
            password=password,
            phone=phone,
            address=address
        )

        if user is None:

            error(
                "Registration failed."
            )

            return None

        success(
            "Customer registration successful."
        )

        return user

    except ValueError as exc:

        error(
            str(exc)
        )

        return None

    except Exception as exc:

        error(
            f"Registration failed: {exc}"
        )

        return None


# ============================================================
# Admin Registration
# ============================================================

def register_admin() -> Optional[User]:
    """
    Display administrator registration form
    and create a new administrator account.

    Returns:
        User object if registration succeeds,
        otherwise None.
    """

    console.print(
        "\n[bold red]=== Admin Registration ===[/bold red]\n"
    )

    try:

        name = get_text(
            "Enter name: "
        )

        email = get_text(
            "Enter email: "
        )

        password = get_text(
            "Enter password: "
        )

        phone = get_text(
            "Enter phone: "
        )

        address = get_text(
            "Enter address: "
        )

        user = User(
            name=name,
            email=email,
            password=password,
            phone=phone,
            address=address,
            role="admin"
        )

        created_user = UserService.create_user(
            user
        )

        if created_user is None:

            error(
                "Admin registration failed."
            )

            return None

        success(
            "Admin registration successful."
        )

        return created_user

    except ValueError as exc:

        error(
            str(exc)
        )

        return None

    except Exception as exc:

        error(
            f"Admin registration failed: {exc}"
        )

        return None


# ============================================================
# Login
# ============================================================

def login_user() -> Optional[User]:
    """
    Display login form and authenticate a user.

    Returns:
        User object if login succeeds,
        otherwise None.
    """

    console.print(
        "\n[bold cyan]=== Login ===[/bold cyan]\n"
    )

    try:

        email = get_text(
            "Enter email: "
        )

        password = get_text(
            "Enter password: "
        )

        user = AuthService.login(
            email=email,
            password=password
        )

        if user is None:

            error(
                "Invalid email or password."
            )

            return None

        success(
            f"Welcome, {user.name}!"
        )

        return user

    except ValueError as exc:

        error(
            str(exc)
        )

        return None

    except Exception as exc:

        error(
            f"Login failed: {exc}"
        )

        return None


# ============================================================
# Logout
# ============================================================

def logout_user(
    user: Optional[User]
) -> None:
    """
    Log out the current user.

    Args:
        user: Currently authenticated user.
    """

    if user is None:
        return

    success(
        f"Goodbye, {user.name}!"
    )