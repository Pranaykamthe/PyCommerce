"""
test_ui_integration.py
----------------------
Integration tests for the PyCommerce UI layer.
"""

from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import patch

from utils.input_helper import (
    get_decimal,
    get_integer,
    get_text,
    get_yes_no,
)
from utils.loading import show_loading
from utils.menu import Menu
from utils.messages import (
    error,
    info,
    success,
    warning,
)
from utils.tables import (
    show_cart_table,
    show_customer_table,
    show_order_table,
    show_product_table,
)
from utils.ui import (
    show_banner,
    show_goodbye,
    show_header,
    show_panel,
    show_welcome,
)


def test_ui_display_components():
    """Test all major UI display components."""

    show_banner()

    show_header(
        "Dashboard",
        "PyCommerce dashboard",
    )

    show_panel(
        "Information",
        "UI integration test",
    )

    show_welcome()
    show_goodbye()


def test_message_components():
    """Test all message utilities."""

    success("Operation completed successfully.")
    error("Something went wrong.")
    warning("This is a warning.")
    info("This is information.")


def test_table_components():
    """Test all table utilities."""

    products = [
        SimpleNamespace(
            product_id=1,
            name="Laptop",
            price=50000.00,
            stock=10,
        )
    ]

    customers = [
        SimpleNamespace(
            customer_id=1,
            name="Test Customer",
            email="customer@example.com",
        )
    ]

    orders = [
        SimpleNamespace(
            order_id=1001,
            customer_id=1,
            total_amount=50000.00,
            status="Completed",
        )
    ]

    cart_items = [
        SimpleNamespace(
            product_id=1,
            product_name="Laptop",
            quantity=1,
            price=50000.00,
        )
    ]

    show_product_table(products)
    show_customer_table(customers)
    show_order_table(orders)
    show_cart_table(cart_items)


def test_input_components():
    """Test input utilities together."""

    with patch(
        "utils.input_helper.console.input",
        return_value="Laptop",
    ):
        product_name = get_text("Product name:")

    assert product_name == "Laptop"

    with patch(
        "utils.input_helper.console.input",
        return_value="10",
    ):
        quantity = get_integer("Quantity:")

    assert quantity == 10

    with patch(
        "utils.input_helper.console.input",
        return_value="499.99",
    ):
        price = get_decimal("Price:")

    assert price == Decimal("499.99")

    with patch(
        "utils.input_helper.console.input",
        return_value="yes",
    ):
        confirmed = get_yes_no("Confirm?")

    assert confirmed is True


def test_loading_component():
    """Test loading utility with a sample operation."""

    def load_products():
        return ["Laptop", "Mouse"]

    result = show_loading(
        "Loading products...",
        load_products,
    )

    assert result == ["Laptop", "Mouse"]


def test_menu_component():
    """Test menu integration."""

    executed = []

    def show_products():
        executed.append("products")

    def show_orders():
        executed.append("orders")

    menu = Menu("PyCommerce Menu")

    menu.add_option(
        "Products",
        show_products,
    )

    menu.add_option(
        "Orders",
        show_orders,
    )

    assert len(menu.options) == 2

    with patch(
        "utils.menu.get_integer",
        return_value=1,
    ):
        menu.run_once()

    assert executed == ["products"]