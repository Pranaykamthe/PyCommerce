import pytest

from services.order_service import OrderService


def test_valid_quantity():
    OrderService.validate_quantity(2)


def test_zero_quantity():
    with pytest.raises(ValueError):
        OrderService.validate_quantity(0)


def test_negative_quantity():
    with pytest.raises(ValueError):
        OrderService.validate_quantity(-1)


def test_calculate_item_total():
    total = OrderService.calculate_item_total(
        price=100,
        quantity=3
    )

    assert total == 300


def test_negative_price():
    with pytest.raises(ValueError):
        OrderService.calculate_item_total(
            price=-100,
            quantity=2
        )


def test_calculate_order_total():
    total = OrderService.calculate_order_total(
        [100, 200, 300]
    )

    assert total == 600


def test_empty_order():
    with pytest.raises(ValueError):
        OrderService.calculate_order_total([])


def test_negative_item_total():
    with pytest.raises(ValueError):
        OrderService.calculate_order_total(
            [100, -50]
        )


def test_valid_order():
    OrderService.validate_order(
        customer_id=1,
        item_totals=[100, 200]
    )


def test_invalid_customer_id():
    with pytest.raises(ValueError):
        OrderService.validate_order(
            customer_id=0,
            item_totals=[100]
        )


def test_order_without_items():
    with pytest.raises(ValueError):
        OrderService.validate_order(
            customer_id=1,
            item_totals=[]
        )