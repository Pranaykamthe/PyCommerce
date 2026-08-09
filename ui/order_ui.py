"""
User interface for order management in PyCommerce.
"""

from models.order import Order
from models.order_item import OrderItem
from models.payment import Payment

from services.order_service import OrderService
from services.cart_service import CartService
from services.payment_service import PaymentService
from services.product_service import ProductService

from repositories.product_repository import ProductRepository

from utils.console import console
from utils.messages import success, error


# ============================================================
# Display Orders
# ============================================================

def display_orders(
    orders: list[Order]
) -> None:
    """Display all orders."""

    console.print(
        "\n[bold cyan]=== My Orders ===[/bold cyan]\n"
    )

    if not orders:

        console.print(
            "[yellow]No orders found.[/yellow]"
        )

        return

    console.print(
        f"{'Order ID':<15}"
        f"{'Total':<15}"
        f"{'Status':<15}"
    )

    console.print(
        "-" * 45
    )

    for order in orders:

        console.print(
            f"{str(order.order_id):<15}"
            f"₹{float(order.total_amount):<14.2f}"
            f"{order.status:<15}"
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
        f"Order ID: {order.order_id}"
    )

    console.print(
        f"User ID: {order.user_id}"
    )

    console.print(
        f"Status: {order.status}"
    )

    console.print(
        f"Shipping Address: {order.shipping_address}"
    )

    console.print(
        f"Total Amount: ₹{float(order.total_amount):.2f}"
    )

    console.print(
        f"Order Date: {order.created_at}"
    )

    console.print(
        "\n[bold]Order Items[/bold]\n"
    )

    if not items:

        console.print(
            "[yellow]No order items found.[/yellow]"
        )

        return

    console.print(
        f"{'Item ID':<12}"
        f"{'Product ID':<15}"
        f"{'Quantity':<12}"
        f"{'Unit Price':<15}"
        f"{'Subtotal':<15}"
    )

    console.print(
        "-" * 70
    )

    for item in items:

        price = float(item.price)

        subtotal = (
            price *
            item.quantity
        )

        console.print(
            f"{str(item.order_item_id):<12}"
            f"{str(item.product_id):<15}"
            f"{str(item.quantity):<12}"
            f"₹{price:<14.2f}"
            f"₹{subtotal:<14.2f}"
        )


# ============================================================
# View My Orders
# ============================================================

def view_my_orders(
    user_id: int
) -> list[Order]:
    """Display all orders belonging to the logged-in user."""

    try:

        orders = OrderService.get_user_orders(
            user_id
        )

        display_orders(
            orders
        )

        return orders

    except ValueError as exc:

        error(
            str(exc)
        )

        return []

    except Exception as exc:

        error(
            f"Unable to load orders: {exc}"
        )

        return []


# ============================================================
# View Order Details
# ============================================================

def view_order_details(
    user_id: int
) -> None:
    """Display details of a selected order."""

    console.print(
        "\n[bold cyan]=== View Order Details ===[/bold cyan]\n"
    )

    try:

        order_id = int(
            input(
                "Enter order ID: "
            ).strip()
        )

        if order_id <= 0:

            raise ValueError(
                "Order ID must be greater than zero."
            )

        order = OrderService.get_order(
            order_id
        )

        if order is None:

            error(
                "Order not found."
            )

            return

        # ----------------------------------------------------
        # Verify ownership
        # ----------------------------------------------------

        if order.user_id != user_id:

            error(
                "You are not authorized to view this order."
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

        error(
            str(exc)
        )

    except Exception as exc:

        error(
            f"Unable to load order details: {exc}"
        )


# ============================================================
# Calculate Cart Total
# ============================================================

def calculate_cart_total(
    items
) -> float:
    """Calculate total amount of cart items."""

    total = 0.0

    for item in items:

        price = float(item.price)

        total += (
            price *
            item.quantity
        )

    return round(
        total,
        2
    )


# ============================================================
# Display Checkout Items
# ============================================================

def display_checkout_items(
    items
) -> None:
    """Display cart items during checkout."""

    console.print(
        f"{'Product ID':<15}"
        f"{'Quantity':<12}"
        f"{'Unit Price':<15}"
        f"{'Subtotal':<15}"
    )

    console.print(
        "-" * 60
    )

    for item in items:

        price = float(item.price)

        subtotal = (
            price *
            item.quantity
        )

        console.print(
            f"{str(item.product_id):<15}"
            f"{str(item.quantity):<12}"
            f"₹{price:<14.2f}"
            f"₹{subtotal:<14.2f}"
        )


# ============================================================
# Check Stock Before Checkout
# ============================================================

def check_stock(
    cart_items
) -> bool:
    """
    Check whether enough stock is available
    for every cart item.
    """

    for item in cart_items:

        if item.product_id is None:

            error(
                "Invalid product ID in cart."
            )

            return False

        product = ProductRepository.get_by_id(
            item.product_id
        )

        if product is None:

            error(
                f"Product {item.product_id} not found."
            )

            return False

        if item.quantity > product.stock:

            error(
                f"Only {product.stock} item(s) "
                f"of product {product.name} "
                "are available."
            )

            return False

    return True


# ============================================================
# Create Order
# ============================================================

def create_order(
    user_id: int
) -> bool:
    """Create an order from the user's shopping cart."""

    console.print(
        "\n[bold cyan]=== Checkout ===[/bold cyan]\n"
    )

    try:

        # ----------------------------------------------------
        # Get Cart
        # ----------------------------------------------------

        cart_items = CartService.get_cart(
            user_id
        )

        if not cart_items:

            error(
                "Your cart is empty."
            )

            return False

        # ----------------------------------------------------
        # Check Stock
        # ----------------------------------------------------

        if not check_stock(
            cart_items
        ):

            return False

        # ----------------------------------------------------
        # Calculate Total
        # ----------------------------------------------------

        total_amount = calculate_cart_total(
            cart_items
        )

        # ----------------------------------------------------
        # Display Cart
        # ----------------------------------------------------

        display_checkout_items(
            cart_items
        )

        console.print(
            "-" * 60
        )

        console.print(
            f"[bold]Total Amount: "
            f"₹{total_amount:.2f}[/bold]"
        )

        # ----------------------------------------------------
        # Shipping Address
        # ----------------------------------------------------

        shipping_address = input(
            "\nEnter shipping address: "
        ).strip()

        if not shipping_address:

            error(
                "Shipping address cannot be empty."
            )

            return False

        # ----------------------------------------------------
        # Confirm Order
        # ----------------------------------------------------

        confirmation = input(
            "Place this order? (y/n): "
        ).strip().lower()

        if confirmation != "y":

            console.print(
                "[yellow]Order cancelled.[/yellow]"
            )

            return False

        # ----------------------------------------------------
        # Prepare Order Items
        # ----------------------------------------------------

        items = []

        for cart_item in cart_items:

            order_item = OrderItem(
                order_id=None,
                product_id=cart_item.product_id,
                quantity=cart_item.quantity,
                price=float(cart_item.price)
            )

            items.append(
                order_item
            )

        # ----------------------------------------------------
        # Create Pending Order
        # ----------------------------------------------------

        order = Order(
            user_id=user_id,
            total_amount=total_amount,
            status="pending",
            shipping_address=shipping_address
        )

        created_order = OrderService.create_order(
            order,
            items
        )

        if created_order is None:

            error(
                "Unable to create order."
            )

            return False

        # ----------------------------------------------------
        # Payment
        # ----------------------------------------------------

        payment = process_payment(
            created_order,
            total_amount
        )

        if payment is None:

            console.print(
                "[yellow]Order remains pending "
                "because payment was not completed.[/yellow]"
            )

            return False

        # ----------------------------------------------------
        # Decrease Stock
        # ----------------------------------------------------

        stock_updated = []

        for cart_item in cart_items:

            if cart_item.product_id is None:

                error(
                    "Invalid product ID."
                )

                return False

            result = ProductRepository.decrease_stock(
                product_id=cart_item.product_id,
                quantity=cart_item.quantity
            )

            if not result:

                # Try to restore stock for items that
                # were already successfully decreased.

                for product_id, quantity in stock_updated:

                    product = ProductRepository.get_by_id(
                        product_id
                    )

                    if product is not None:

                        ProductService.increase_stock(
                            product,
                            quantity
                        )

                        ProductRepository.update(
                            product
                        )

                error(
                    f"Unable to decrease stock "
                    f"for product {cart_item.product_id}."
                )

                return False

            stock_updated.append(
                (
                    cart_item.product_id,
                    cart_item.quantity
                )
            )

        # ----------------------------------------------------
        # Clear Cart
        # ----------------------------------------------------

        cart_cleared = CartService.clear_cart(
            user_id
        )

        if not cart_cleared:

            # The order and stock are already processed.
            # Do not fail the order because the cart is
            # already empty.

            console.print(
                "[yellow]Warning: Cart was already empty "
                "after checkout.[/yellow]"
            )

        # ----------------------------------------------------
        # Confirm Order
        # ----------------------------------------------------

        confirmed = OrderService.update_order_status(
            created_order.order_id,
            "confirmed"
        )

        if not confirmed:

            error(
                "Payment completed, but order could not "
                "be confirmed."
            )

            return False

        # ----------------------------------------------------
        # Success
        # ----------------------------------------------------

        success(
            f"Order #{created_order.order_id} "
            "placed successfully."
        )

        console.print(
            f"Payment ID: {payment.payment_id}"
        )

        console.print(
            f"Payment Status: {payment.status}"
        )

        console.print(
            f"Total Amount: ₹{total_amount:.2f}"
        )

        return True

    except ValueError as exc:

        error(
            str(exc)
        )

        return False

    except Exception as exc:

        error(
            f"Unable to create order: {exc}"
        )

        return False


# ============================================================
# Process Payment
# ============================================================

def process_payment(
    order: Order,
    amount: float
) -> Payment | None:
    """Create and process a payment."""

    console.print(
        "\n[bold cyan]=== Payment ===[/bold cyan]\n"
    )

    console.print(
        f"Amount Payable: ₹{amount:.2f}\n"
    )

    console.print(
        "Payment Methods"
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

    choice = input(
        "\nEnter payment method: "
    ).strip()

    payment_methods = {
        "1": "cash",
        "2": "card",
        "3": "upi",
        "4": "net_banking"
    }

    if choice not in payment_methods:

        error(
            "Invalid payment method."
        )

        return None

    payment_method = payment_methods[
        choice
    ]

    display_method = {
        "cash": "cash",
        "card": "card",
        "upi": "upi",
        "net_banking": "net banking"
    }

    console.print(
        f"\nPayment Method: "
        f"{display_method[payment_method]}"
    )

    console.print(
        f"Amount: ₹{amount:.2f}"
    )

    confirmation = input(
        "Confirm payment? (y/n): "
    ).strip().lower()

    if confirmation != "y":

        console.print(
            "[yellow]Payment cancelled.[/yellow]"
        )

        return None

    try:

        # ----------------------------------------------------
        # Create Payment Object
        # ----------------------------------------------------

        payment = Payment(
            order_id=order.order_id,
            amount=amount,
            payment_method=payment_method,
            status="successful"
        )

        # ----------------------------------------------------
        # Save Payment
        # ----------------------------------------------------

        created_payment = PaymentService.create_payment(
            payment
        )

        if created_payment is None:

            error(
                "Payment failed."
            )

            return None

        success(
            "Payment completed successfully."
        )

        console.print(
            f"Payment ID: {created_payment.payment_id}"
        )

        console.print(
            f"Payment Status: {created_payment.status}"
        )

        return created_payment

    except ValueError as exc:

        error(
            str(exc)
        )

        return None

    except Exception as exc:

        error(
            f"Unable to process payment: {exc}"
        )

        return None


# ============================================================
# Cancel Order
# ============================================================

def cancel_order(
    user_id: int
) -> bool:
    """Cancel an order and restore product stock."""

    console.print(
        "\n[bold cyan]=== Cancel Order ===[/bold cyan]\n"
    )

    try:

        # ----------------------------------------------------
        # Get Order ID
        # ----------------------------------------------------

        order_id = int(
            input(
                "Enter order ID: "
            ).strip()
        )

        if order_id <= 0:

            raise ValueError(
                "Order ID must be greater than zero."
            )

        # ----------------------------------------------------
        # Find Order
        # ----------------------------------------------------

        order = OrderService.get_order(
            order_id
        )

        if order is None:

            error(
                "Order not found."
            )

            return False

        # ----------------------------------------------------
        # Verify Ownership
        # ----------------------------------------------------

        if order.user_id != user_id:

            error(
                "You are not authorized to cancel this order."
            )

            return False

        # ----------------------------------------------------
        # Check Status
        # ----------------------------------------------------

        if order.status == "cancelled":

            error(
                "This order is already cancelled."
            )

            return False

        if order.status == "delivered":

            error(
                "Delivered orders cannot be cancelled."
            )

            return False

        # ----------------------------------------------------
        # Show Order
        # ----------------------------------------------------

        console.print(
            f"\nOrder ID: {order.order_id}"
        )

        console.print(
            f"Total: ₹{float(order.total_amount):.2f}"
        )

        console.print(
            f"Status: {order.status}"
        )

        # ----------------------------------------------------
        # Confirm Cancellation
        # ----------------------------------------------------

        confirmation = input(
            "\nCancel this order? (y/n): "
        ).strip().lower()

        if confirmation != "y":

            console.print(
                "[yellow]Order cancellation cancelled.[/yellow]"
            )

            return False

        # ----------------------------------------------------
        # Get Order Items
        # ----------------------------------------------------

        order_items = OrderService.get_order_items(
            order_id
        )

        if not order_items:

            error(
                "No order items found."
            )

            return False

        # ----------------------------------------------------
        # Restore Stock
        # ----------------------------------------------------

        for item in order_items:

            if item.product_id is None:

                error(
                    "Invalid product ID in order."
                )

                return False

            product = ProductRepository.get_by_id(
                item.product_id
            )

            if product is None:

                error(
                    f"Product {item.product_id} not found."
                )

                return False

            # Increase stock in the Product object.

            ProductService.increase_stock(
                product,
                item.quantity
            )

            # Persist the changed stock to MySQL.

            updated = ProductRepository.update(
                product
            )

            if not updated:

                error(
                    f"Unable to restore stock "
                    f"for product {item.product_id}."
                )

                return False

        # ----------------------------------------------------
        # Cancel Order
        # ----------------------------------------------------

        cancelled = OrderService.update_order_status(
            order_id,
            "cancelled"
        )

        if not cancelled:

            error(
                "Unable to cancel order."
            )

            return False

        success(
            "Order cancelled successfully."
        )

        success(
            "Product stock restored successfully."
        )

        return True

    except ValueError as exc:

        error(
            str(exc)
        )

        return False

    except Exception as exc:

        error(
            f"Unable to cancel order: {exc}"
        )

        return False


# ============================================================
# Order Menu
# ============================================================

def order_menu(
    user_id: int
) -> None:
    """Display the order management menu."""

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
            "5. Back"
        )

        choice = input(
            "\nEnter your choice: "
        ).strip()

        if choice == "1":

            view_my_orders(
                user_id
            )

        elif choice == "2":

            view_order_details(
                user_id
            )

        elif choice == "3":

            create_order(
                user_id
            )

        elif choice == "4":

            cancel_order(
                user_id
            )

        elif choice == "5":

            break

        else:

            error(
                "Invalid choice."
            )