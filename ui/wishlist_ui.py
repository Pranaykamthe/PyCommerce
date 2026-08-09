"""
Wishlist user interface for PyCommerce.
"""

from models.wishlist import Wishlist

from services.wishlist_service import WishlistService

from utils.console import console
from utils.messages import success, error


# ============================================================
# Display Wishlist
# ============================================================

def display_wishlist(
    items: list[Wishlist]
) -> None:
    """Display all items in the wishlist."""

    console.print(
        "\n[bold cyan]=== My Wishlist ===[/bold cyan]\n"
    )

    if not items:

        console.print(
            "[yellow]Your wishlist is empty.[/yellow]"
        )

        return

    console.print(
        "[bold]"
        f"{'Wishlist ID':<15}"
        f"{'Product ID':<15}"
        f"{'Added At':<25}"
        "[/bold]"
    )

    console.print(
        "-" * 55
    )

    for item in items:

        wishlist_id = item.wishlist_id
        product_id = item.product_id
        added_at = item.added_at or "N/A"

        console.print(
            f"{str(wishlist_id):<15}"
            f"{str(product_id):<15}"
            f"{str(added_at):<25}"
        )


# ============================================================
# View Wishlist
# ============================================================

def view_wishlist(
    user_id: int
) -> list[Wishlist]:
    """Load and display a user's wishlist."""

    try:

        items = WishlistService.get_wishlist(
            user_id
        )

        display_wishlist(
            items
        )

        return items

    except ValueError as exc:

        error(
            str(exc)
        )

        return []

    except Exception as exc:

        error(
            f"Unable to load wishlist: {exc}"
        )

        return []


# ============================================================
# Add Product
# ============================================================

def add_to_wishlist(
    user_id: int
) -> bool:
    """Add a product to the user's wishlist."""

    console.print(
        "\n[bold cyan]=== Add To Wishlist ===[/bold cyan]\n"
    )

    try:

        product_id = int(
            input(
                "Product ID: "
            ).strip()
        )

        result = WishlistService.add_to_wishlist(
            user_id=user_id,
            product_id=product_id
        )

        if result:

            success(
                "Product added to wishlist."
            )

            return True

        error(
            "Unable to add product to wishlist."
        )

        return False

    except ValueError as exc:

        error(
            str(exc)
        )

        return False

    except Exception as exc:

        error(
            f"Unable to add product to wishlist: {exc}"
        )

        return False


# ============================================================
# Remove Product
# ============================================================

def remove_from_wishlist(
    user_id: int
) -> bool:
    """Remove a product from the user's wishlist."""

    console.print(
        "\n[bold cyan]=== Remove From Wishlist ===[/bold cyan]\n"
    )

    try:

        product_id = int(
            input(
                "Product ID: "
            ).strip()
        )

        result = WishlistService.remove_from_wishlist(
            user_id=user_id,
            product_id=product_id
        )

        if result:

            success(
                "Product removed from wishlist."
            )

            return True

        error(
            "Unable to remove product from wishlist."
        )

        return False

    except ValueError as exc:

        error(
            str(exc)
        )

        return False

    except Exception as exc:

        error(
            f"Unable to remove product from wishlist: {exc}"
        )

        return False


# ============================================================
# Clear Wishlist
# ============================================================

def clear_wishlist(
    user_id: int
) -> bool:
    """Remove all products from the user's wishlist."""

    console.print(
        "\n[bold cyan]=== Clear Wishlist ===[/bold cyan]"
    )

    confirmation = input(
        "Are you sure you want to clear the wishlist? (y/n): "
    ).strip().lower()

    if confirmation != "y":

        console.print(
            "[yellow]Clear wishlist cancelled.[/yellow]"
        )

        return False

    try:

        result = WishlistService.clear_wishlist(
            user_id
        )

        if result:

            success(
                "Wishlist cleared successfully."
            )

            return True

        error(
            "Unable to clear wishlist."
        )

        return False

    except ValueError as exc:

        error(
            str(exc)
        )

        return False

    except Exception as exc:

        error(
            f"Unable to clear wishlist: {exc}"
        )

        return False


# ============================================================
# Wishlist Menu
# ============================================================

def wishlist_menu(
    user_id: int
) -> None:
    """Display the customer's wishlist menu."""

    while True:

        console.print(
            "\n[bold cyan]=== Wishlist ===[/bold cyan]"
        )

        console.print(
            "1. View Wishlist"
        )

        console.print(
            "2. Add Product"
        )

        console.print(
            "3. Remove Product"
        )

        console.print(
            "4. Clear Wishlist"
        )

        console.print(
            "0. Back"
        )

        choice = input(
            "\nEnter your choice: "
        ).strip()

        if choice == "1":

            view_wishlist(
                user_id
            )

        elif choice == "2":

            add_to_wishlist(
                user_id
            )

        elif choice == "3":

            remove_from_wishlist(
                user_id
            )

        elif choice == "4":

            clear_wishlist(
                user_id
            )

        elif choice == "0":

            break

        else:

            error(
                "Invalid choice."
            )