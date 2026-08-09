"""
Order-related user interface for PyCommerce.
"""

from ui.payment_ui import PaymentUI

from models.order import Order
from models.order_item import OrderItem

from services.order_service import OrderService
from services.cart_service import CartService

from repositories.product_repository import ProductRepository

from utils.console import console
from utils.messages import success, error


# ============================================================
# Display Orders
# ============================================================

def display_orders(
    orders: list[Order]
) -> None:
    """Display a list of orders."""

    console.print(
        "\n[bold cyan]=== My Orders ===[/bold cyan]\n"
    )

    if not orders:
        console.print(
            "[yellow]No orders found.[/yellow]"
        )
        return

    console.print(
        f"{'Order ID':<12}"
        f"{'Total':<15}"
        f"{'Status':<15}"
    )

    console.print("-" * 45)

    for order in orders:
        console.print(
            f"{str(order.order_id):<12}"
            f"₹{order.total_amount:<14.2f}"
            f"{order.status:<15}"
        )


# ============================================================
# View User Orders
# ============================================================

def view_my_orders(
    user_id: int
) -> None:
    """Display all orders belonging to the current user."""

    try:
        orders = OrderService.get_user_orders(
            user_id
        )

        display_orders(orders)

    except ValueError as exc:
        error(str(exc))

    except Exception as exc:
        error(
            f"Unable to load orders: {exc}"
        )


# ============================================================
# Display Order Details
# ============================================================

def display_order_details(
    order: Order,
    items: list[OrderItem]
) -> None:
    """Display complete order details."""

    console.print(
        "\n[bold cyan]=== Order Details ===[/bold cyan]\n"
    )

    console.print(
        f"[bold]Order ID:[/bold] "
        f"{order.order_id}"
    )

    console.print(
        f"[bold]User ID:[/bold] "
        f"{order.user_id}"
    )

    console.print(
        f"[bold]Status:[/bold] "
        f"{order.status}"
    )

    console.print(
        f"[bold]Shipping Address:[/bold] "
        f"{order.shipping_address}"
    )

    console.print(
        f"[bold]Total Amount:[/bold] "
        f"₹{order.total_amount:.2f}"
    )

    if order.created_at:
        console.print(
            f"[bold]Order Date:[/bold] "
            f"{order.created_at}"
        )

    console.print(
        "\n[bold]Order Items[/bold]"
    )

    if not items:
        console.print(
            "[yellow]No order items found.[/yellow]"
        )
        return

    console.print(
        f"\n{'Item ID':<10}"
        f"{'Product ID':<15}"
        f"{'Quantity':<12}"
        f"{'Unit Price':<15}"
        f"{'Subtotal':<15}"
    )

    console.print("-" * 67)

    for item in items:

        subtotal = (
            item.quantity *
            item.price
        )

        console.print(
            f"{str(item.order_item_id):<10}"
            f"{str(item.product_id):<15}"
            f"{str(item.quantity):<12}"
            f"₹{item.price:<14.2f}"
            f"₹{subtotal:<14.2f}"
        )


# ============================================================
# View Order Details
# ============================================================

def view_order_details() -> None:
    """Ask for an order ID and display its details."""

    console.print(
        "\n[bold cyan]=== View Order Details ===[/bold cyan]\n"
    )

    try:
        order_id = int(
            input(
                "Enter order ID: "
            ).strip()
        )

        order = OrderService.get_order(
            order_id
        )

        if order is None:
            error(
                "Order not found."
            )
            return

        items = OrderService.get_order_items(
            order_id
        )

        display_order_details(
            order,
            items
        )

    except ValueError as exc:
        error(str(exc))

    except Exception as exc:
        error(
            f"Unable to load order: {exc}"
        )


# ============================================================
# Create Order From Cart
# ============================================================

def create_order_ui(
    user_id: int
) -> None:
    """
    Create an order using the current user's shopping cart
    and process payment.
    """

    console.print(
        "\n[bold cyan]=== Checkout ===[/bold cyan]\n"
    )

    try:

        # ----------------------------------------------------
        # Get cart
        # ----------------------------------------------------

        cart_items = CartService.get_cart(
            user_id
        )

        if not cart_items:
            error(
                "Your shopping cart is empty."
            )
            return

        # ----------------------------------------------------
        # Display cart items
        # ----------------------------------------------------

        console.print(
            f"{'Product ID':<15}"
            f"{'Quantity':<12}"
            f"{'Unit Price':<15}"
            f"{'Subtotal':<15}"
        )

        console.print("-" * 57)

        total_amount = 0.0

        order_items: list[OrderItem] = []

        for cart_item in cart_items:

            product = ProductRepository.get_by_id(
                cart_item.product_id
            )

            if product is None:
                error(
                    f"Product {cart_item.product_id} "
                    "was not found."
                )
                return

            # ------------------------------------------------
            # Check stock before creating order
            # ------------------------------------------------

            if cart_item.quantity > product.stock:
                error(
                    f"Only {product.stock} item(s) "
                    f"of product {product.product_id} "
                    "are available."
                )
                return

            subtotal = (
                cart_item.quantity *
                product.price
            )

            total_amount += subtotal

            console.print(
                f"{str(cart_item.product_id):<15}"
                f"{str(cart_item.quantity):<12}"
                f"₹{product.price:<14.2f}"
                f"₹{subtotal:<14.2f}"
            )

            order_items.append(
                OrderItem(
                    product_id=cart_item.product_id,
                    quantity=cart_item.quantity,
                    price=product.price
                )
            )

        console.print("-" * 57)

        console.print(
            f"Total Amount: "
            f"₹{total_amount:.2f}"
        )

        # ----------------------------------------------------
        # Shipping address
        # ----------------------------------------------------

        shipping_address = input(
            "\nEnter shipping address: "
        ).strip()

        if not shipping_address:
            error(
                "Shipping address cannot be empty."
            )
            return

        # ----------------------------------------------------
        # Order confirmation
        # ----------------------------------------------------

        confirmation = input(
            "Place this order? (y/n): "
        ).strip().lower()

        if confirmation != "y":
            console.print(
                "[yellow]Order cancelled.[/yellow]"
            )
            return

        # ----------------------------------------------------
        # Create order
        # ----------------------------------------------------

        order = Order(
            user_id=user_id,
            status="pending",
            shipping_address=shipping_address
        )

        created_order = OrderService.create_order(
            order,
            order_items
        )

        if created_order is None:
            error(
                "Unable to create order."
            )
            return

        # ----------------------------------------------------
        # Payment
        # ----------------------------------------------------

        payment = PaymentUI.process_payment(
            order_id=created_order.order_id,
            amount=created_order.total_amount
        )

        # ----------------------------------------------------
        # Payment failed / cancelled
        # ----------------------------------------------------

        if payment is None:
            error(
                f"Payment was not completed for "
                f"Order #{created_order.order_id}."
            )

            console.print(
                "[yellow]"
                "Your order remains pending."
                "[/yellow]"
            )

            return

        # ----------------------------------------------------
        # Payment successful
        # ----------------------------------------------------

        # Clear cart only after successful payment.
        cart_cleared = CartService.clear_cart(
            user_id
        )

        if not cart_cleared:
            console.print(
                "[yellow]"
                "Payment successful, but the cart "
                "could not be cleared."
                "[/yellow]"
            )

        # ----------------------------------------------------
        # Update order status
        # ----------------------------------------------------

        try:
            OrderService.update_order_status(
                created_order.order_id,
                "confirmed"
            )

            created_order.status = "confirmed"

        except Exception:
            # Payment has already succeeded, so do not
            # report the entire checkout as failed.
            console.print(
                "[yellow]"
                "Payment succeeded, but order status "
                "could not be updated."
                "[/yellow]"
            )

        # ----------------------------------------------------
        # Final confirmation
        # ----------------------------------------------------

        success(
            f"Order #{created_order.order_id} "
            "placed successfully."
        )

        console.print(
            f"Payment ID: "
            f"{payment.payment_id}"
        )

        console.print(
            f"Payment Status: "
            f"{payment.status}"
        )

        console.print(
            f"Total Amount: "
            f"₹{created_order.total_amount:.2f}"
        )

    except ValueError as exc:
        error(str(exc))

    except Exception as exc:
        error(
            f"Unable to create order: {exc}"
        )


# ============================================================
# Cancel Order
# ============================================================

def cancel_order(
    user_id: int
) -> None:
    """Cancel an order belonging to the current user."""

    console.print(
        "\n[bold cyan]=== Cancel Order ===[/bold cyan]\n"
    )

    try:
        order_id = int(
            input(
                "Enter order ID: "
            ).strip()
        )

        order = OrderService.get_order(
            order_id
        )

        if order is None:
            error(
                "Order not found."
            )
            return

        if order.user_id != user_id:
            error(
                "You cannot modify another user's order."
            )
            return

        if order.status in {
            "shipped",
            "delivered",
            "cancelled"
        }:
            error(
                f"Order cannot be cancelled "
                f"because its status is "
                f"'{order.status}'."
            )
            return

        result = OrderService.update_order_status(
            order_id,
            "cancelled"
        )

        if result:
            success(
                "Order cancelled successfully."
            )
        else:
            error(
                "Unable to cancel order."
            )

    except ValueError as exc:
        error(str(exc))

    except Exception as exc:
        error(
            f"Unable to cancel order: {exc}"
        )


# ============================================================
# Order Menu
# ============================================================

def order_menu(
    user_id: int
) -> None:
    """Display the customer order menu."""

    while True:

        console.print(
            "\n[bold cyan]=== Order Menu ===[/bold cyan]"
        )

        console.print(
            "1. View My Orders"
        )

        console.print(
            "2. View Order Details"
        )

        console.print(
            "3. Create Order"
        )

        console.print(
            "4. Cancel Order"
        )

        console.print(
            "0. Back"
        )

        choice = input(
            "\nEnter your choice: "
        ).strip()

        if choice == "1":
            view_my_orders(
                user_id
            )

        elif choice == "2":
            view_order_details()

        elif choice == "3":
            create_order_ui(
                user_id
            )

        elif choice == "4":
            cancel_order(
                user_id
            )

        elif choice == "0":
            break

        else:
            error(
                "Invalid choice."
            )


# ============================================================
# Admin Order Status
# ============================================================

def update_order_status_ui() -> None:
    """Update the status of an order."""

    console.print(
        "\n[bold cyan]=== Update Order Status ===[/bold cyan]\n"
    )

    console.print(
        "Allowed statuses:"
    )

    console.print(
        "pending, confirmed, shipped, "
        "delivered, cancelled"
    )

    try:
        order_id = int(
            input(
                "Enter order ID: "
            ).strip()
        )

        status = input(
            "Enter new status: "
        ).strip().lower()

        result = OrderService.update_order_status(
            order_id,
            status
        )

        if result:
            success(
                "Order status updated successfully."
            )
        else:
            error(
                "Order not found or could not be updated."
            )

    except ValueError as exc:
        error(str(exc))

    except Exception as exc:
        error(
            f"Unable to update order status: {exc}"
        )


# ============================================================
# Admin Delete Order
# ============================================================

def delete_order_ui() -> None:
    """Delete an order."""

    console.print(
        "\n[bold cyan]=== Delete Order ===[/bold cyan]"
    )

    try:
        order_id = int(
            input(
                "Enter order ID: "
            ).strip()
        )

        order = OrderService.get_order(
            order_id
        )

        if order is None:
            error(
                "Order not found."
            )
            return

        console.print(
            f"Order #{order.order_id}"
        )

        console.print(
            f"Total: ₹{order.total_amount:.2f}"
        )

        console.print(
            f"Status: {order.status}"
        )

        confirmation = input(
            "Delete this order? (y/n): "
        ).strip().lower()

        if confirmation != "y":
            console.print(
                "[yellow]Deletion cancelled.[/yellow]"
            )
            return

        result = OrderService.delete_order(
            order_id
        )

        if result:
            success(
                "Order deleted successfully."
            )
        else:
            error(
                "Unable to delete order."
            )

    except ValueError as exc:
        error(str(exc))

    except Exception as exc:
        error(
            f"Unable to delete order: {exc}"
        )


# ============================================================
# Admin Order Menu
# ============================================================

def order_admin_menu() -> None:
    """Display order management menu for administrators."""

    while True:

        console.print(
            "\n[bold cyan]=== Order Management ===[/bold cyan]"
        )

        console.print(
            "1. View Order Details"
        )

        console.print(
            "2. Update Order Status"
        )

        console.print(
            "3. Delete Order"
        )

        console.print(
            "0. Back"
        )

        choice = input(
            "\nEnter your choice: "
        ).strip()

        if choice == "1":
            view_order_details()

        elif choice == "2":
            update_order_status_ui()

        elif choice == "3":
            delete_order_ui()

        elif choice == "0":
            break

        else:
            error(
                "Invalid choice."
            )