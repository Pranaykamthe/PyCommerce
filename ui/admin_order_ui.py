"""
Admin order management UI.

Provides admin operations for viewing,
updating, and deleting customer orders.
"""

from services.order_service import OrderService
from utils.input_helper import get_integer, get_choice
from utils.messages import success, error
from utils.ui import show_header
from rich.table import Table
from utils.console import console

def admin_order_menu() -> None:
    """
    Display the admin order management menu.
    """

    while True:

        show_header("Order Management")

        print("1. View All Orders")
        print("2. View Order Details")
        print("3. Update Order Status")
        print("4. Delete Order")
        print("5. Back")

        choice = get_choice(
            "Enter your choice: ",
            ["1", "2", "3", "4", "5"]
        )

        if choice == "1":
            view_all_orders()

        elif choice == "2":
            view_order_details()

        elif choice == "3":
            update_order_status()

        elif choice == "4":
            delete_order()

        elif choice == "5":
            break


# ============================================================
# View All Orders
# ============================================================

def view_all_orders() -> None:
    """
    Display all orders in the system.

    Uses get_user_orders() for each user only when
    a user ID is available from the order records.
    """

    show_header("All Orders")

    try:
        # ----------------------------------------------------
        # Since OrderService does not expose get_all_orders(),
        # retrieve orders using known user IDs.
        # ----------------------------------------------------

        from repositories.user_repository import UserRepository

        users = UserRepository.get_all()

        orders = []

        for user in users:

            if user.user_id is None:
                continue

            user_orders = OrderService.get_user_orders(
                user.user_id
            )

            orders.extend(user_orders)

        if not orders:
            console.print(
                "[yellow]No orders available.[/yellow]"
            )
            return

        table = Table(
            title="Orders"
        )

        table.add_column(
            "Order ID",
            justify="center"
        )

        table.add_column(
            "User ID",
            justify="center"
        )

        table.add_column(
            "Total",
            justify="right"
        )

        table.add_column(
            "Status",
            justify="center"
        )

        table.add_column(
            "Shipping Address"
        )

        for order in orders:

            table.add_row(
                str(order.order_id),
                str(order.user_id),
                f"₹{order.total_amount:.2f}",
                order.status,
                order.shipping_address
            )

        console.print(table)

    except Exception as exc:

        error(
            f"Unable to load orders: {exc}"
        )


# ============================================================
# View Order Details
# ============================================================

def view_order_details() -> None:
    """
    Display complete information about an order
    and its order items.
    """

    show_header("View Order Details")

    order_id = get_integer(
        "Enter order ID: "
    )

    try:

        order = OrderService.get_order(
            order_id
        )

        if order is None:

            error(
                "Order not found."
            )

            return

        console.print()
        console.print(
            f"[bold cyan]Order ID:[/bold cyan] "
            f"{order.order_id}"
        )

        console.print(
            f"[bold cyan]User ID:[/bold cyan] "
            f"{order.user_id}"
        )

        console.print(
            f"[bold cyan]Status:[/bold cyan] "
            f"{order.status}"
        )

        console.print(
            f"[bold cyan]Shipping Address:[/bold cyan] "
            f"{order.shipping_address}"
        )

        console.print(
            f"[bold cyan]Total Amount:[/bold cyan] "
            f"₹{order.total_amount:.2f}"
        )

        console.print()

        items = OrderService.get_order_items(
            order_id
        )

        if not items:

            console.print(
                "[yellow]No order items found.[/yellow]"
            )

            return

        table = Table(
            title="Order Items"
        )

        table.add_column(
            "Item ID",
            justify="center"
        )

        table.add_column(
            "Product ID",
            justify="center"
        )

        table.add_column(
            "Quantity",
            justify="center"
        )

        table.add_column(
            "Unit Price",
            justify="right"
        )

        table.add_column(
            "Subtotal",
            justify="right"
        )

        for item in items:

            subtotal = (
                item.quantity *
                item.price
            )

            table.add_row(
                str(item.order_item_id),
                str(item.product_id),
                str(item.quantity),
                f"₹{item.price:.2f}",
                f"₹{subtotal:.2f}"
            )

        console.print(table)

    except ValueError as exc:

        error(
            str(exc)
        )

    except Exception as exc:

        error(
            f"Unable to view order: {exc}"
        )


# ============================================================
# Update Order Status
# ============================================================

def update_order_status() -> None:
    """
    Update the status of an existing order.
    """

    show_header("Update Order Status")

    order_id = get_integer(
        "Enter order ID: "
    )

    try:

        order = OrderService.get_order(
            order_id
        )

        if order is None:

            error(
                "Order not found."
            )

            return

        console.print(
            f"Current status: "
            f"[bold yellow]{order.status}[/bold yellow]"
        )

        statuses = OrderService.ALLOWED_STATUSES

        console.print(
            "\nAvailable statuses:"
        )

        for status in statuses:

            console.print(
                f"- {status}"
            )

        new_status = get_choice(
            "Enter new status: ",
            list(statuses)
        )

        updated = OrderService.update_order_status(
            order_id=order_id,
            status=new_status
        )

        if updated:

            success(
                "Order status updated successfully."
            )

        else:

            error(
                "Unable to update order status."
            )

    except ValueError as exc:

        error(
            str(exc)
        )

    except Exception as exc:

        error(
            f"Unable to update order status: {exc}"
        )


# ============================================================
# Delete Order
# ============================================================

def delete_order() -> None:
    """
    Delete an order from the system.
    """

    show_header("Delete Order")

    order_id = get_integer(
        "Enter order ID: "
    )

    try:

        order = OrderService.get_order(
            order_id
        )

        if order is None:

            error(
                "Order not found."
            )

            return

        console.print(
            f"\nOrder ID: {order.order_id}"
        )

        console.print(
            f"User ID: {order.user_id}"
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
                "[yellow]Delete cancelled.[/yellow]"
            )

            return

        deleted = OrderService.delete_order(
            order_id
        )

        if deleted:

            success(
                "Order deleted successfully."
            )

        else:

            error(
                "Unable to delete order."
            )

    except ValueError as exc:

        error(
            str(exc)
        )

    except Exception as exc:

        error(
            f"Unable to delete order: {exc}"
        )