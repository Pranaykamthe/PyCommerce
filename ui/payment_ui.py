"""
User interface for payment operations.
"""

from models.payment import Payment
from services.payment_service import PaymentService

from utils.messages import (
    success,
    error,
    warning
)


class PaymentUI:
    """Handles customer payment interactions."""

    # ========================================================
    # Payment
    # ========================================================

    @staticmethod
    def process_payment(
        order_id: int,
        amount: float
    ) -> Payment | None:
        """
        Process payment for an order.
        """

        print("\n=== Payment ===\n")

        print(
            f"Amount Payable: ₹{amount:.2f}"
        )

        print("\nPayment Methods")

        print("1. Cash")
        print("2. Card")
        print("3. UPI")
        print("4. Net Banking")

        try:
            choice = input(
                "\nEnter payment method: "
            ).strip()

            methods = {
                "1": "cash",
                "2": "card",
                "3": "upi",
                "4": "net_banking"
            }

            payment_method = methods.get(
                choice
            )

            if payment_method is None:
                error(
                    "Invalid payment method."
                )
                return None

            transaction_id = None

            # ------------------------------------------------
            # Transaction ID
            # ------------------------------------------------

            if payment_method != "cash":
                transaction_id = input(
                    "Enter transaction ID: "
                ).strip()

                if not transaction_id:
                    error(
                        "Transaction ID is required."
                    )
                    return None

            # ------------------------------------------------
            # Confirmation
            # ------------------------------------------------

            print(
                f"\nPayment Method: "
                f"{payment_method}"
            )

            print(
                f"Amount: ₹{amount:.2f}"
            )

            confirm = input(
                "Confirm payment? (y/n): "
            ).strip().lower()

            if confirm != "y":
                warning(
                    "Payment cancelled."
                )
                return None

            # ------------------------------------------------
            # Create payment
            # ------------------------------------------------

            payment = Payment(
                order_id=order_id,
                payment_method=payment_method,
                transaction_id=transaction_id,
                amount=amount,
                status="successful"
            )

            created_payment = (
                PaymentService.create_payment(
                    payment
                )
            )

            if created_payment is None:
                error(
                    "Unable to process payment."
                )
                return None

            success(
                "Payment completed successfully."
            )

            print(
                f"Payment ID: "
                f"{created_payment.payment_id}"
            )

            print(
                f"Payment Status: "
                f"{created_payment.status}"
            )

            return created_payment

        except ValueError as exc:
            error(
                f"Payment failed: {exc}"
            )

            return None

        except Exception as exc:
            error(
                f"Unable to process payment: {exc}"
            )

            return None

    # ========================================================
    # View Payment
    # ========================================================

    @staticmethod
    def view_payment(
        order_id: int
    ) -> None:
        """
        Display payment information for an order.
        """

        print("\n=== Payment Details ===\n")

        try:
            payment = (
                PaymentService.get_payment_by_order(
                    order_id
                )
            )

            if payment is None:
                warning(
                    "No payment found for this order."
                )
                return

            print(
                f"Payment ID: "
                f"{payment.payment_id}"
            )

            print(
                f"Order ID: "
                f"{payment.order_id}"
            )

            print(
                f"Payment Method: "
                f"{payment.payment_method}"
            )

            print(
                f"Payment Status: "
                f"{payment.status}"
            )

            print(
                f"Transaction ID: "
                f"{payment.transaction_id or 'N/A'}"
            )

            print(
                f"Amount: "
                f"₹{payment.amount:.2f}"
            )

            if payment.paid_at:
                print(
                    f"Payment Date: "
                    f"{payment.paid_at}"
                )

        except ValueError as exc:
            error(
                f"Unable to view payment: {exc}"
            )

        except Exception as exc:
            error(
                f"Unable to view payment: {exc}"
            )