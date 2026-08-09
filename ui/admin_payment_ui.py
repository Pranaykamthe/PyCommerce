"""
Admin payment management UI.

Provides administrator operations for viewing,
updating, and deleting customer payments.
"""

from rich.table import Table

from services.payment_service import PaymentService

from utils.console import console
from utils.messages import success, error, warning
from utils.input_helper import get_integer, get_choice
from utils.ui import show_header


# ============================================================
# Admin Payment Menu
# ============================================================

def admin_payment_menu() -> None:
    """
    Display the admin payment management menu.
    """

    while True:

        show_header("Payment Management")

        print("1. View All Payments")
        print("2. View Payment Details")
        print("3. Find Payment by Order")
        print("4. Update Payment Status")
        print("5. Delete Payment")
        print("6. Back")

        choice = get_choice(
            "Enter your choice: ",
            ["1", "2", "3", "4", "5", "6"]
        )

        if choice == "1":
            view_all_payments()

        elif choice == "2":
            view_payment_details()

        elif choice == "3":
            view_payment_by_order()

        elif choice == "4":
            update_payment_status()

        elif choice == "5":
            delete_payment()

        elif choice == "6":
            break


# ============================================================
# View All Payments
# ============================================================

def view_all_payments() -> None:
    """
    Display all payments in the system.
    """

    show_header("All Payments")

    try:

        payments = PaymentService.get_all_payments()

        if not payments:

            console.print(
                "[yellow]No payments available.[/yellow]"
            )

            return

        table = Table(
            title="Payments"
        )

        table.add_column(
            "Payment ID",
            justify="center"
        )

        table.add_column(
            "Order ID",
            justify="center"
        )

        table.add_column(
            "Method",
            justify="center"
        )

        table.add_column(
            "Status",
            justify="center"
        )

        table.add_column(
            "Amount",
            justify="right"
        )

        table.add_column(
            "Transaction ID"
        )

        for payment in payments:

            table.add_row(
                str(payment.payment_id),
                str(payment.order_id),
                payment.payment_method,
                payment.status,
                f"₹{payment.amount:.2f}",
                payment.transaction_id or "N/A"
            )

        console.print(table)

    except Exception as exc:

        error(
            f"Unable to load payments: {exc}"
        )


# ============================================================
# View Payment Details
# ============================================================

def view_payment_details() -> None:
    """
    Display complete information about a payment.
    """

    show_header("Payment Details")

    payment_id = get_integer(
        "Enter payment ID: "
    )

    try:

        payment = PaymentService.get_payment(
            payment_id
        )

        if payment is None:

            error(
                "Payment not found."
            )

            return

        console.print()

        console.print(
            f"[bold cyan]Payment ID:[/bold cyan] "
            f"{payment.payment_id}"
        )

        console.print(
            f"[bold cyan]Order ID:[/bold cyan] "
            f"{payment.order_id}"
        )

        console.print(
            f"[bold cyan]Payment Method:[/bold cyan] "
            f"{payment.payment_method}"
        )

        console.print(
            f"[bold cyan]Payment Status:[/bold cyan] "
            f"{payment.status}"
        )

        console.print(
            f"[bold cyan]Transaction ID:[/bold cyan] "
            f"{payment.transaction_id or 'N/A'}"
        )

        console.print(
            f"[bold cyan]Amount:[/bold cyan] "
            f"₹{payment.amount:.2f}"
        )

        if payment.paid_at:

            console.print(
                f"[bold cyan]Payment Date:[/bold cyan] "
                f"{payment.paid_at}"
            )

    except ValueError as exc:

        error(
            str(exc)
        )

    except Exception as exc:

        error(
            f"Unable to view payment: {exc}"
        )


# ============================================================
# Find Payment By Order
# ============================================================

def view_payment_by_order() -> None:
    """
    Find and display the payment associated
    with an order.
    """

    show_header("Payment By Order")

    order_id = get_integer(
        "Enter order ID: "
    )

    try:

        payment = PaymentService.get_payment_by_order(
            order_id
        )

        if payment is None:

            warning(
                "No payment found for this order."
            )

            return

        console.print()

        console.print(
            f"[bold cyan]Payment ID:[/bold cyan] "
            f"{payment.payment_id}"
        )

        console.print(
            f"[bold cyan]Order ID:[/bold cyan] "
            f"{payment.order_id}"
        )

        console.print(
            f"[bold cyan]Payment Method:[/bold cyan] "
            f"{payment.payment_method}"
        )

        console.print(
            f"[bold cyan]Payment Status:[/bold cyan] "
            f"{payment.status}"
        )

        console.print(
            f"[bold cyan]Transaction ID:[/bold cyan] "
            f"{payment.transaction_id or 'N/A'}"
        )

        console.print(
            f"[bold cyan]Amount:[/bold cyan] "
            f"₹{payment.amount:.2f}"
        )

        if payment.paid_at:

            console.print(
                f"[bold cyan]Payment Date:[/bold cyan] "
                f"{payment.paid_at}"
            )

    except ValueError as exc:

        error(
            str(exc)
        )

    except Exception as exc:

        error(
            f"Unable to find payment: {exc}"
        )


# ============================================================
# Update Payment Status
# ============================================================

def update_payment_status() -> None:
    """
    Update the status of an existing payment.
    """

    show_header("Update Payment Status")

    payment_id = get_integer(
        "Enter payment ID: "
    )

    try:

        payment = PaymentService.get_payment(
            payment_id
        )

        if payment is None:

            error(
                "Payment not found."
            )

            return

        console.print(
            f"Current status: "
            f"[bold yellow]{payment.status}[/bold yellow]"
        )

        statuses = list(
            PaymentService.ALLOWED_STATUSES
        )

        console.print(
            "\nAvailable statuses:"
        )

        for status in statuses:

            console.print(
                f"- {status}"
            )

        new_status = get_choice(
            "Enter new status: ",
            statuses
        )

        updated = PaymentService.update_payment_status(
            payment_id=payment_id,
            status=new_status
        )

        if updated:

            success(
                "Payment status updated successfully."
            )

        else:

            error(
                "Unable to update payment status."
            )

    except ValueError as exc:

        error(
            str(exc)
        )

    except Exception as exc:

        error(
            f"Unable to update payment status: {exc}"
        )


# ============================================================
# Delete Payment
# ============================================================

def delete_payment() -> None:
    """
    Delete a payment from the system.
    """

    show_header("Delete Payment")

    payment_id = get_integer(
        "Enter payment ID: "
    )

    try:

        payment = PaymentService.get_payment(
            payment_id
        )

        if payment is None:

            error(
                "Payment not found."
            )

            return

        console.print()

        console.print(
            f"Payment ID: {payment.payment_id}"
        )

        console.print(
            f"Order ID: {payment.order_id}"
        )

        console.print(
            f"Payment Method: {payment.payment_method}"
        )

        console.print(
            f"Payment Status: {payment.status}"
        )

        console.print(
            f"Amount: ₹{payment.amount:.2f}"
        )

        confirmation = input(
            "\nDelete this payment? (y/n): "
        ).strip().lower()

        if confirmation != "y":

            console.print(
                "[yellow]Deletion cancelled.[/yellow]"
            )

            return

        deleted = PaymentService.delete_payment(
            payment_id
        )

        if deleted:

            success(
                "Payment deleted successfully."
            )

        else:

            error(
                "Unable to delete payment."
            )

    except ValueError as exc:

        error(
            str(exc)
        )

    except Exception as exc:

        error(
            f"Unable to delete payment: {exc}"
        )