"""
Administrator interface for PyCommerce.
"""

from models.user import User

from services.user_service import UserService

from ui.product_ui import product_admin_menu
from ui.admin_order_ui import admin_order_menu
from ui.admin_payment_ui import admin_payment_menu
from ui.auth_ui import logout_user

from utils.console import console
from utils.messages import success, error


# ============================================================
# Display Users
# ============================================================

def display_users(
    users: list[User]
) -> None:
    """Display all active users."""

    console.print(
        "\n[bold cyan]=== User Management ===[/bold cyan]\n"
    )

    if not users:
        console.print(
            "[yellow]No users found.[/yellow]"
        )
        return

    console.print(
        f"{'ID':<8}"
        f"{'Name':<25}"
        f"{'Email':<35}"
        f"{'Role':<12}"
    )

    console.print("-" * 80)

    for user in users:

        console.print(
            f"{str(user.user_id):<8}"
            f"{user.name:<25}"
            f"{user.email:<35}"
            f"{user.role:<12}"
        )


# ============================================================
# View All Users
# ============================================================

def view_users() -> None:
    """Display all active users."""

    try:

        users = UserService.get_all_users()

        display_users(users)

    except Exception as exc:

        error(
            f"Unable to load users: {exc}"
        )


# ============================================================
# View User
# ============================================================

def view_user() -> None:
    """Display one user by ID."""

    console.print(
        "\n[bold cyan]=== View User ===[/bold cyan]\n"
    )

    try:

        user_id = int(
            input(
                "Enter user ID: "
            ).strip()
        )

        user = UserService.get_user(
            user_id
        )

        if user is None:

            error(
                "User not found."
            )

            return

        console.print(
            f"\n[bold]User ID:[/bold] "
            f"{user.user_id}"
        )

        console.print(
            f"[bold]Name:[/bold] "
            f"{user.name}"
        )

        console.print(
            f"[bold]Email:[/bold] "
            f"{user.email}"
        )

        console.print(
            f"[bold]Phone:[/bold] "
            f"{user.phone}"
        )

        console.print(
            f"[bold]Address:[/bold] "
            f"{user.address}"
        )

        console.print(
            f"[bold]Role:[/bold] "
            f"{user.role}"
        )

        if user.created_at:

            console.print(
                f"[bold]Created:[/bold] "
                f"{user.created_at}"
            )

    except ValueError as exc:

        error(
            str(exc)
        )

    except Exception as exc:

        error(
            f"Unable to load user: {exc}"
        )


# ============================================================
# Create User
# ============================================================

def create_user_ui() -> None:
    """Create a new user from the admin interface."""

    console.print(
        "\n[bold cyan]=== Create User ===[/bold cyan]\n"
    )

    try:

        name = input(
            "Name: "
        ).strip()

        email = input(
            "Email: "
        ).strip()

        password = input(
            "Password: "
        ).strip()

        phone = input(
            "Phone: "
        ).strip()

        address = input(
            "Address: "
        ).strip()

        role = input(
            "Role (customer/admin): "
        ).strip().lower()

        user = User(
            name=name,
            email=email,
            password=password,
            phone=phone,
            address=address,
            role=role
        )

        created_user = UserService.create_user(
            user
        )

        if created_user is None:

            error(
                "Unable to create user."
            )

            return

        success(
            f"User '{created_user.name}' "
            "created successfully."
        )

    except ValueError as exc:

        error(
            str(exc)
        )

    except Exception as exc:

        error(
            f"Unable to create user: {exc}"
        )


# ============================================================
# Update User
# ============================================================

def update_user_ui() -> None:
    """Update an existing user."""

    console.print(
        "\n[bold cyan]=== Update User ===[/bold cyan]\n"
    )

    try:

        user_id = int(
            input(
                "Enter user ID: "
            ).strip()
        )

        user = UserService.get_user(
            user_id
        )

        if user is None:

            error(
                "User not found."
            )

            return

        console.print(
            f"\nCurrent name: {user.name}"
        )

        name = input(
            "New name "
            "(press Enter to keep current): "
        ).strip()

        if name:

            user.name = name

        console.print(
            f"Current email: {user.email}"
        )

        email = input(
            "New email "
            "(press Enter to keep current): "
        ).strip()

        if email:

            user.email = email

        console.print(
            f"Current phone: {user.phone}"
        )

        phone = input(
            "New phone "
            "(press Enter to keep current): "
        ).strip()

        if phone:

            user.phone = phone

        console.print(
            f"Current address: {user.address}"
        )

        address = input(
            "New address "
            "(press Enter to keep current): "
        ).strip()

        if address:

            user.address = address

        console.print(
            f"Current role: {user.role}"
        )

        role = input(
            "New role "
            "(customer/admin, Enter to keep current): "
        ).strip().lower()

        if role:

            user.role = role

        # UserService.update_user() expects
        # the existing password hash.

        result = UserService.update_user(
            user
        )

        if result:

            success(
                "User updated successfully."
            )

        else:

            error(
                "Unable to update user."
            )

    except ValueError as exc:

        error(
            str(exc)
        )

    except Exception as exc:

        error(
            f"Unable to update user: {exc}"
        )


# ============================================================
# Delete User
# ============================================================

def delete_user_ui(
    current_admin_id: int
) -> None:
    """Soft-delete a user."""

    console.print(
        "\n[bold cyan]=== Delete User ===[/bold cyan]\n"
    )

    try:

        user_id = int(
            input(
                "Enter user ID: "
            ).strip()
        )

        if user_id == current_admin_id:

            error(
                "You cannot delete your own account."
            )

            return

        user = UserService.get_user(
            user_id
        )

        if user is None:

            error(
                "User not found."
            )

            return

        console.print(
            f"\nUser ID: {user.user_id}"
        )

        console.print(
            f"Name: {user.name}"
        )

        console.print(
            f"Email: {user.email}"
        )

        console.print(
            f"Role: {user.role}"
        )

        confirmation = input(
            "\nDelete this user? (y/n): "
        ).strip().lower()

        if confirmation != "y":

            console.print(
                "[yellow]Deletion cancelled.[/yellow]"
            )

            return

        result = UserService.delete_user(
            user_id
        )

        if result:

            success(
                "User deleted successfully."
            )

        else:

            error(
                "Unable to delete user."
            )

    except ValueError as exc:

        error(
            str(exc)
        )

    except Exception as exc:

        error(
            f"Unable to delete user: {exc}"
        )


# ============================================================
# User Management Menu
# ============================================================

def user_management_menu(
    current_admin_id: int
) -> None:
    """Display user management options."""

    while True:

        console.print(
            "\n[bold cyan]=== User Management ===[/bold cyan]"
        )

        console.print(
            "1. View All Users"
        )

        console.print(
            "2. View User"
        )

        console.print(
            "3. Create User"
        )

        console.print(
            "4. Update User"
        )

        console.print(
            "5. Delete User"
        )

        console.print(
            "0. Back"
        )

        choice = input(
            "\nEnter your choice: "
        ).strip()

        if choice == "1":

            view_users()

        elif choice == "2":

            view_user()

        elif choice == "3":

            create_user_ui()

        elif choice == "4":

            update_user_ui()

        elif choice == "5":

            delete_user_ui(
                current_admin_id
            )

        elif choice == "0":

            break

        else:

            error(
                "Invalid choice."
            )


# ============================================================
# Admin Header
# ============================================================

def display_admin_header(
    admin: User
) -> None:
    """Display administrator information."""

    console.print(
        "\n[bold red]====================================[/bold red]"
    )

    console.print(
        "[bold red]          PyCommerce Admin          [/bold red]"
    )

    console.print(
        "[bold red]====================================[/bold red]"
    )

    console.print(
        f"[bold]Welcome:[/bold] {admin.name}"
    )

    console.print(
        f"[bold]Email:[/bold] {admin.email}"
    )

    console.print(
        f"[bold]Role:[/bold] {admin.role}"
    )


# ============================================================
# Admin Menu
# ============================================================

def admin_menu(
    admin: User
) -> None:
    """Display the main administrator menu."""

    if admin.role != "admin":

        error(
            "Access denied. Administrator privileges required."
        )

        return

    if admin.user_id is None:

        error(
            "Administrator ID is missing."
        )

        return

    while True:

        display_admin_header(
            admin
        )

        console.print(
            "\n[bold]Admin Menu[/bold]"
        )

        console.print(
            "1. Product Management"
        )

        console.print(
            "2. Order Management"
        )

        console.print(
            "3. Payment Management"
        )

        console.print(
            "4. User Management"
        )

        console.print(
            "5. Logout"
        )

        choice = input(
            "\nEnter your choice: "
        ).strip()

        if choice == "1":

            product_admin_menu()

        elif choice == "2":

            admin_order_menu()

        elif choice == "3":

            admin_payment_menu()

        elif choice == "4":

            user_management_menu(
                admin.user_id
            )

        elif choice == "5":

            logout_user(
                admin
            )

            break

        else:

            error(
                "Invalid choice."
            )