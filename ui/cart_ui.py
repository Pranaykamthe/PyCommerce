"""
Shopping cart user interface for PyCommerce.
"""

from models.cart import Cart

from services.cart_service import CartService
from services.checkout_service import CheckoutService

from utils.console import console
from utils.messages import success, error


# ============================================================
# Display Cart
# ============================================================

def display_cart(
    items: list[Cart]
) -> None:
    """Display all items in the shopping cart."""

    console.print(
        "\n[bold cyan]=== Shopping Cart ===[/bold cyan]\n"
    )

    if not items:

        console.print(
            "[yellow]Your cart is empty.[/yellow]"
        )

        return

    console.print(
        "[bold]"
        f"{'Product ID':<15}"
        f"{'Product Name':<20}"
        f"{'Quantity':<12}"
        f"{'Unit Price':<15}"
        f"{'Subtotal':<15}"
        "[/bold]"
    )

    console.print(
        "-" * 77
    )

    total = 0.0

    for item in items:

        product_id = item.product_id
        product_name = item.product_name
        quantity = item.quantity
        price = float(item.price)

        subtotal = price * quantity

        total += subtotal

        console.print(
            f"{str(product_id):<15}"
            f"{product_name:<20}"
            f"{str(quantity):<12}"
            f"₹{price:<14.2f}"
            f"₹{subtotal:<14.2f}"
        )

    console.print(
        "-" * 77
    )

    console.print(
        f"[bold]Total: ₹{total:.2f}[/bold]"
    )


# ============================================================
# View Cart
# ============================================================

def view_cart(
    user_id: int
) -> list[Cart]:
    """Load and display a user's cart."""

    try:

        items = CartService.get_cart(
            user_id
        )

        display_cart(
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
            f"Unable to load cart: {exc}"
        )

        return []


# ============================================================
# Add Product
# ============================================================

def add_to_cart(
    user_id: int
) -> bool:
    """Add a product to the user's cart."""

    console.print(
        "\n[bold cyan]=== Add to Cart ===[/bold cyan]\n"
    )

    try:

        product_id = int(
            input(
                "Product ID: "
            ).strip()
        )

        quantity = int(
            input(
                "Quantity: "
            ).strip()
        )

        result = CartService.add_to_cart(
            user_id=user_id,
            product_id=product_id,
            quantity=quantity
        )

        if result:

            success(
                "Product added to cart."
            )

            return True

        error(
            "Unable to add product to cart."
        )

        return False

    except ValueError as exc:

        error(
            str(exc)
        )

        return False

    except Exception as exc:

        error(
            f"Unable to add product: {exc}"
        )

        return False


# ============================================================
# Update Quantity
# ============================================================

def update_cart_item(
    user_id: int
) -> bool:
    """Update the quantity of a cart item."""

    console.print(
        "\n[bold cyan]=== Update Cart Item ===[/bold cyan]\n"
    )

    try:

        product_id = int(
            input(
                "Product ID: "
            ).strip()
        )

        quantity = int(
            input(
                "New quantity: "
            ).strip()
        )

        result = CartService.update_quantity(
            user_id=user_id,
            product_id=product_id,
            quantity=quantity
        )

        if result:

            success(
                "Cart item updated successfully."
            )

            return True

        error(
            "Unable to update cart item."
        )

        return False

    except ValueError as exc:

        error(
            str(exc)
        )

        return False

    except Exception as exc:

        error(
            f"Unable to update cart: {exc}"
        )

        return False


# ============================================================
# Remove Item
# ============================================================

def remove_from_cart(
    user_id: int
) -> bool:
    """Remove a product from the user's cart."""

    console.print(
        "\n[bold cyan]=== Remove Cart Item ===[/bold cyan]\n"
    )

    try:

        product_id = int(
            input(
                "Product ID: "
            ).strip()
        )

        result = CartService.remove_from_cart(
            user_id=user_id,
            product_id=product_id
        )

        if result:

            success(
                "Product removed from cart."
            )

            return True

        error(
            "Unable to remove product from cart."
        )

        return False

    except ValueError as exc:

        error(
            str(exc)
        )

        return False

    except Exception as exc:

        error(
            f"Unable to remove product: {exc}"
        )

        return False


# ============================================================
# Checkout
# ============================================================

def checkout(
    user_id: int
) -> bool:
    """Complete the checkout process."""

    console.print(
        "\n[bold cyan]=== Checkout ===[/bold cyan]\n"
    )

    try:

        # ----------------------------------------------------
        # Check cart
        # ----------------------------------------------------

        items = CartService.get_cart(
            user_id
        )

        if not items:

            error(
                "Your cart is empty."
            )

            return False

        display_cart(
            items
        )

        # ----------------------------------------------------
        # Shipping address
        # ----------------------------------------------------

        shipping_address = input(
            "\nShipping Address: "
        ).strip()

        # ----------------------------------------------------
        # Payment method
        # ----------------------------------------------------

        console.print(
            "\n[bold]Payment Method[/bold]"
        )

        console.print(
            "1. Cash"
        )

        console.print(
            "2. Card"
        )

        console.print(
            "3. UPI"
        )

        console.print(
            "4. Net Banking"
        )

        payment_choice = input(
            "\nChoose payment method: "
        ).strip()

        payment_methods = {
            "1": "cash",
            "2": "card",
            "3": "upi",
            "4": "net_banking"
        }

        payment_method = payment_methods.get(
            payment_choice
        )

        if payment_method is None:

            error(
                "Invalid payment method."
            )

            return False

        # ----------------------------------------------------
        # Confirm checkout
        # ----------------------------------------------------

        confirmation = input(
            "\nConfirm order? (y/n): "
        ).strip().lower()

        if confirmation != "y":

            console.print(
                "[yellow]Checkout cancelled.[/yellow]"
            )

            return False

        # ----------------------------------------------------
        # Process checkout
        # ----------------------------------------------------

        result = CheckoutService.checkout(
            user_id=user_id,
            shipping_address=shipping_address,
            payment_method=payment_method
        )

        if result is None:

            error(
                "Unable to complete checkout."
            )

            return False

        order = result["order"]
        payment = result["payment"]

        # ----------------------------------------------------
        # Confirmation
        # ----------------------------------------------------

        console.print(
            "\n[bold green]"
            "=== Order Confirmed ==="
            "[/bold green]\n"
        )

        console.print(
            f"Order ID: {order.order_id}"
        )

        console.print(
            f"Payment ID: {payment.payment_id}"
        )

        console.print(
            f"Payment Method: "
            f"{payment.payment_method}"
        )

        console.print(
            f"Payment Status: "
            f"{payment.status}"
        )

        console.print(
            f"Order Status: "
            f"{order.status}"
        )

        console.print(
            f"Total: ₹{order.total_amount:.2f}"
        )

        success(
            "Order placed successfully."
        )

        return True

    except ValueError as exc:

        error(
            str(exc)
        )

        return False

    except Exception as exc:

        error(
            f"Unable to complete checkout: {exc}"
        )

        return False


# ============================================================
# Clear Cart
# ============================================================

def clear_cart(
    user_id: int
) -> bool:
    """Remove all items from the user's cart."""

    console.print(
        "\n[bold cyan]=== Clear Cart ===[/bold cyan]"
    )

    confirmation = input(
        "Are you sure you want to clear the cart? (y/n): "
    ).strip().lower()

    if confirmation != "y":

        console.print(
            "[yellow]Clear cart cancelled.[/yellow]"
        )

        return False

    try:

        result = CartService.clear_cart(
            user_id
        )

        if result:

            success(
                "Cart cleared successfully."
            )

            return True

        error(
            "Unable to clear cart."
        )

        return False

    except ValueError as exc:

        error(
            str(exc)
        )

        return False

    except Exception as exc:

        error(
            f"Unable to clear cart: {exc}"
        )

        return False


# ============================================================
# Cart Menu
# ============================================================

def cart_menu(
    user_id: int
) -> None:
    """Display the shopping cart menu."""

    while True:

        console.print(
            "\n[bold cyan]=== Shopping Cart ===[/bold cyan]"
        )

        console.print(
            "1. View Cart"
        )

        console.print(
            "2. Add Product"
        )

        console.print(
            "3. Update Quantity"
        )

        console.print(
            "4. Remove Product"
        )

        console.print(
            "5. Checkout"
        )

        console.print(
            "6. Clear Cart"
        )

        console.print(
            "0. Back"
        )

        choice = input(
            "\nEnter your choice: "
        ).strip()

        if choice == "1":

            view_cart(
                user_id
            )

        elif choice == "2":

            add_to_cart(
                user_id
            )

        elif choice == "3":

            update_cart_item(
                user_id
            )

        elif choice == "4":

            remove_from_cart(
                user_id
            )

        elif choice == "5":

            checkout(
                user_id
            )

        elif choice == "6":

            clear_cart(
                user_id
            )

        elif choice == "0":

            break

        else:

            error(
                "Invalid choice."
            )
