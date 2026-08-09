"""
main_ui.py
----------
Main application interface for PyCommerce.
"""

from models.user import User

from ui.auth_ui import (
    login_user,
    register_user,
    register_admin,
)

from ui.customer_ui import customer_menu
from ui.admin_ui import admin_menu

from utils.console import console
from utils.messages import error


# ============================================================
# Application Header
# ============================================================

def display_header() -> None:
    """Display the PyCommerce application header."""

    console.print(
        "\n[bold cyan]========================================[/bold cyan]"
    )

    console.print(
        "[bold cyan]             PyCommerce               [/bold cyan]"
    )

    console.print(
        "[bold cyan]       E-Commerce Console System       [/bold cyan]"
    )

    console.print(
        "[bold cyan]========================================[/bold cyan]"
    )


# ============================================================
# Main Welcome Menu
# ============================================================

def display_welcome_menu() -> None:
    """Display the main welcome menu."""

    console.print(
        "\n[bold]Main Menu[/bold]"
    )

    console.print(
        "1. Admin"
    )

    console.print(
        "2. Customer"
    )

    console.print(
        "0. Exit"
    )


# ============================================================
# Admin Authentication Menu
# ============================================================

def admin_auth_menu() -> None:
    """Display the administrator login and registration menu."""

    while True:

        console.print(
            "\n[bold red]=== Admin ===[/bold red]"
        )

        console.print(
            "1. Login"
        )

        console.print(
            "2. Register"
        )

        console.print(
            "3. Back to Main Menu"
        )

        choice = input(
            "\nEnter your choice: "
        ).strip()

        # ----------------------------------------------------
        # Admin Login
        # ----------------------------------------------------

        if choice == "1":

            user = login_user()

            if user is None:
                continue

            if user.role != "admin":

                error(
                    "Access denied. "
                    "Please use the Customer menu."
                )

                continue

            admin_menu(
                user
            )

        # ----------------------------------------------------
        # Admin Registration
        # ----------------------------------------------------

        elif choice == "2":

            register_admin()

        # ----------------------------------------------------
        # Back
        # ----------------------------------------------------

        elif choice == "3":

            break

        else:

            error(
                "Invalid choice."
            )


# ============================================================
# Customer Authentication Menu
# ============================================================

def customer_auth_menu() -> None:
    """Display the customer login and registration menu."""

    while True:

        console.print(
            "\n[bold cyan]=== Customer ===[/bold cyan]"
        )

        console.print(
            "1. Login"
        )

        console.print(
            "2. Register"
        )

        console.print(
            "3. Back to Main Menu"
        )

        choice = input(
            "\nEnter your choice: "
        ).strip()

        # ----------------------------------------------------
        # Customer Login
        # ----------------------------------------------------

        if choice == "1":

            user = login_user()

            if user is None:
                continue

            if user.role != "customer":

                error(
                    "Please use the Admin menu "
                    "for administrator accounts."
                )

                continue

            customer_menu(
                user
            )

        # ----------------------------------------------------
        # Customer Registration
        # ----------------------------------------------------

        elif choice == "2":

            register_user()

        # ----------------------------------------------------
        # Back
        # ----------------------------------------------------

        elif choice == "3":

            break

        else:

            error(
                "Invalid choice."
            )


# ============================================================
# Main Application
# ============================================================

def run_application() -> None:
    """Run the PyCommerce console application."""

    while True:

        display_header()

        display_welcome_menu()

        choice = input(
            "\nEnter your choice: "
        ).strip()

        # ----------------------------------------------------
        # Admin
        # ----------------------------------------------------

        if choice == "1":

            admin_auth_menu()

        # ----------------------------------------------------
        # Customer
        # ----------------------------------------------------

        elif choice == "2":

            customer_auth_menu()

        # ----------------------------------------------------
        # Exit
        # ----------------------------------------------------

        elif choice == "0":

            console.print(
                "\n[bold green]"
                "Thank you for using PyCommerce!"
                "[/bold green]"
            )

            break

        # ----------------------------------------------------
        # Invalid Choice
        # ----------------------------------------------------

        else:

            error(
                "Invalid choice."
            )


# ============================================================
# Entry Point
# ============================================================

if __name__ == "__main__":
    run_application()