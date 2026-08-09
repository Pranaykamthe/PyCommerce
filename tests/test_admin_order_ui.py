"""
Tests for Admin Order Management UI.
"""

from unittest.mock import patch

from models.order import Order
from models.order_item import OrderItem

from ui.admin_order_ui import (
    admin_order_menu,
    view_all_orders,
    view_order_details,
    update_order_status,
    delete_order,
)


# ============================================================
# View All Orders
# ============================================================


def test_view_all_orders():
    """Test displaying all orders."""

    order = Order(
        order_id=100,
        user_id=1,
        total_amount=1500.00,
        status="confirmed",
        shipping_address="Pune"
    )

    mock_user = type(
        "User",
        (),
        {
            "user_id": 1
        }
    )()

    with patch(
        "repositories.user_repository.UserRepository.get_all",
        return_value=[mock_user]
    ), patch(
        "ui.admin_order_ui.OrderService.get_user_orders",
        return_value=[order]
    ):

        view_all_orders()


def test_view_all_orders_empty():
    """Test displaying orders when none exist."""

    with patch(
        "repositories.user_repository.UserRepository.get_all",
        return_value=[]
    ):

        view_all_orders()


# ============================================================
# View Order Details
# ============================================================


def test_view_order_details():
    """Test displaying order details."""

    order = Order(
        order_id=100,
        user_id=1,
        total_amount=1500.00,
        status="confirmed",
        shipping_address="Pune"
    )

    item = OrderItem(
        order_item_id=1,
        order_id=100,
        product_id=10,
        quantity=2,
        price=750.00
    )

    with patch(
        "ui.admin_order_ui.get_integer",
        return_value=100
    ), patch(
        "ui.admin_order_ui.OrderService.get_order",
        return_value=order
    ), patch(
        "ui.admin_order_ui.OrderService.get_order_items",
        return_value=[item]
    ):

        view_order_details()


def test_view_order_details_not_found():
    """Test viewing a nonexistent order."""

    with patch(
        "ui.admin_order_ui.get_integer",
        return_value=999999999
    ), patch(
        "ui.admin_order_ui.OrderService.get_order",
        return_value=None
    ):

        view_order_details()


def test_view_order_details_no_items():
    """Test viewing an order with no order items."""

    order = Order(
        order_id=101,
        user_id=1,
        total_amount=500.00,
        status="pending",
        shipping_address="Pune"
    )

    with patch(
        "ui.admin_order_ui.get_integer",
        return_value=101
    ), patch(
        "ui.admin_order_ui.OrderService.get_order",
        return_value=order
    ), patch(
        "ui.admin_order_ui.OrderService.get_order_items",
        return_value=[]
    ):

        view_order_details()


# ============================================================
# Update Order Status
# ============================================================


def test_update_order_status():
    """Test updating an order status."""

    order = Order(
        order_id=100,
        user_id=1,
        total_amount=1500.00,
        status="pending",
        shipping_address="Pune"
    )

    with patch(
        "ui.admin_order_ui.get_integer",
        return_value=100
    ), patch(
        "ui.admin_order_ui.OrderService.get_order",
        return_value=order
    ), patch(
        "ui.admin_order_ui.get_choice",
        return_value="confirmed"
    ), patch(
        "ui.admin_order_ui.OrderService.update_order_status",
        return_value=True
    ) as mock_update:

        update_order_status()

    mock_update.assert_called_once_with(
        order_id=100,
        status="confirmed"
    )


def test_update_order_status_order_not_found():
    """Test updating a nonexistent order."""

    with patch(
        "ui.admin_order_ui.get_integer",
        return_value=999999999
    ), patch(
        "ui.admin_order_ui.OrderService.get_order",
        return_value=None
    ):

        update_order_status()


# ============================================================
# Delete Order
# ============================================================


def test_delete_order():
    """Test deleting an order."""

    order = Order(
        order_id=100,
        user_id=1,
        total_amount=1500.00,
        status="confirmed",
        shipping_address="Pune"
    )

    with patch(
        "ui.admin_order_ui.get_integer",
        return_value=100
    ), patch(
        "ui.admin_order_ui.OrderService.get_order",
        return_value=order
    ), patch(
        "builtins.input",
        return_value="y"
    ), patch(
        "ui.admin_order_ui.OrderService.delete_order",
        return_value=True
    ) as mock_delete:

        delete_order()

    mock_delete.assert_called_once_with(100)


def test_delete_order_cancelled():
    """Test cancelling order deletion."""

    order = Order(
        order_id=101,
        user_id=1,
        total_amount=500.00,
        status="pending",
        shipping_address="Pune"
    )

    with patch(
        "ui.admin_order_ui.get_integer",
        return_value=101
    ), patch(
        "ui.admin_order_ui.OrderService.get_order",
        return_value=order
    ), patch(
        "builtins.input",
        return_value="n"
    ), patch(
        "ui.admin_order_ui.OrderService.delete_order"
    ) as mock_delete:

        delete_order()

    mock_delete.assert_not_called()


def test_delete_order_not_found():
    """Test deleting a nonexistent order."""

    with patch(
        "ui.admin_order_ui.get_integer",
        return_value=999999999
    ), patch(
        "ui.admin_order_ui.OrderService.get_order",
        return_value=None
    ):

        delete_order()


# ============================================================
# Admin Menu
# ============================================================


def test_admin_order_menu_back():
    """Test returning from admin order menu."""

    with patch(
        "ui.admin_order_ui.get_choice",
        return_value="5"
    ):

        admin_order_menu()