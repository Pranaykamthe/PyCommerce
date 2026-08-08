"""
tables.py
---------
Reusable Rich table utilities for PyCommerce.

Provides functions for displaying:
- Products
- Customers
- Orders
- Cart items
"""

from rich.table import Table

from utils.console import console


def create_table(
    title: str,
    columns: list[str],
) -> Table:
    """
    Create a reusable Rich table.

    Args:
        title: Table title.
        columns: List of column names.

    Returns:
        Rich Table object.
    """

    table = Table(
        title=title,
        show_header=True,
        header_style="bold cyan",
        border_style="blue",
    )

    for column in columns:
        table.add_column(column)

    return table


def show_product_table(products: list):
    """
    Display products in a Rich table.

    Expected product attributes:
    product_id, name, price, stock
    """

    table = create_table(
        "Products",
        ["ID", "Name", "Price", "Stock"],
    )

    for product in products:
        table.add_row(
            str(product.product_id),
            str(product.name),
            f"₹{product.price:.2f}",
            str(product.stock),
        )

    console.print(table)


def show_customer_table(customers: list):
    """
    Display customers in a Rich table.

    Expected customer attributes:
    customer_id, name, email
    """

    table = create_table(
        "Customers",
        ["ID", "Name", "Email"],
    )

    for customer in customers:
        table.add_row(
            str(customer.customer_id),
            str(customer.name),
            str(customer.email),
        )

    console.print(table)


def show_order_table(orders: list):
    """
    Display orders in a Rich table.

    Expected order attributes:
    order_id, customer_id, total_amount, status
    """

    table = create_table(
        "Orders",
        ["Order ID", "Customer ID", "Total", "Status"],
    )

    for order in orders:
        table.add_row(
            str(order.order_id),
            str(order.customer_id),
            f"₹{order.total_amount:.2f}",
            str(order.status),
        )

    console.print(table)


def show_cart_table(cart_items: list):
    """
    Display cart items in a Rich table.

    Expected cart item attributes:
    product_id, product_name, quantity, price
    """

    table = create_table(
        "Shopping Cart",
        ["Product ID", "Product", "Quantity", "Price"],
    )

    for item in cart_items:
        table.add_row(
            str(item.product_id),
            str(item.product_name),
            str(item.quantity),
            f"₹{item.price:.2f}",
        )

    console.print(table)