"""
Customer dashboard and menu for PyCommerce.
"""

from models.user import User

from ui.product_ui import product_menu
from ui.cart_ui import cart_menu
from ui.order_ui import order_menu
from ui.auth_ui import logout_user

from utils.console import console
from utils.messages import error


# ============================================================
# Customer Header
# ============================================================

def display_customer_header(
    user: User
) -> None:
    """Display the current customer's information."""

    console.print(
        "\n[bold cyan]====================================[/bold cyan]"
    )

    console.print(
        "[bold cyan]        PyCommerce Customer        [/bold cyan]"
    )

    console.print(
        "[bold cyan]====================================[/bold cyan]"
    )

    console.print(
        f"[bold]Welcome:[/bold] {user.name}"
    )

    console.print(
        f"[bold]Email:[/bold] {user.email}"
    )

    console.print(
        f"[bold]Role:[/bold] {user.role}"
    )


# ============================================================
# Customer Menu
# ============================================================

def customer_menu(
    user: User
) -> None:
    """
    Display the main customer menu.

    The menu remains active until the customer chooses
    logout.
    """

    while True:

        display_customer_header(
            user
        )

        console.print(
            "\n[bold]Customer Menu[/bold]"
        )

        console.print(
            "1. Browse Products"
        )

        console.print(
            "2. Shopping Cart"
        )

        console.print(
            "3. My Orders"
        )

        console.print(
            "4. Logout"
        )

        choice = input(
            "\nEnter your choice: "
        ).strip()

        if choice == "1":

            product_menu(
                user.user_id
            )

        elif choice == "2":

            cart_menu(
                user.user_id
            )

        elif choice == "3":

            order_menu(
                user.user_id
            )

        elif choice == "4":

            logout_user(
                user
            )

            break

        else:

            error(
                "Invalid choice."
            )
