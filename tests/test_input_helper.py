from decimal import Decimal
from unittest.mock import patch

import pytest

from utils.input_helper import (
    get_text,
    get_integer,
    get_decimal,
    get_choice,
    get_yes_no,
)


def test_get_text():
    """Test text input."""

    with patch(
        "utils.input_helper.console.input",
        return_value="Laptop",
    ):
        result = get_text("Enter product name:")

    assert result == "Laptop"


def test_get_integer():
    """Test integer input."""

    with patch(
        "utils.input_helper.console.input",
        return_value="10",
    ):
        result = get_integer("Enter quantity:")

    assert result == 10


def test_get_integer_range():
    """Test integer range validation."""

    with patch(
        "utils.input_helper.console.input",
        side_effect=["0", "5"],
    ):
        result = get_integer(
            "Enter quantity:",
            min_value=1,
            max_value=10,
        )

    assert result == 5


def test_get_decimal():
    """Test decimal input."""

    with patch(
        "utils.input_helper.console.input",
        return_value="499.99",
    ):
        result = get_decimal("Enter price:")

    assert result == Decimal("499.99")


def test_get_decimal_range():
    """Test decimal range validation."""

    with patch(
        "utils.input_helper.console.input",
        side_effect=["-10", "99.99"],
    ):
        result = get_decimal(
            "Enter price:",
            min_value=Decimal("0"),
            max_value=Decimal("1000"),
        )

    assert result == Decimal("99.99")


def test_get_choice():
    """Test choice input."""

    with patch(
        "utils.input_helper.console.input",
        return_value="admin",
    ):
        result = get_choice(
            "Select role:",
            ["admin", "customer"],
        )

    assert result == "admin"


def test_get_choice_case_insensitive():
    """Test case-insensitive choices."""

    with patch(
        "utils.input_helper.console.input",
        return_value="CUSTOMER",
    ):
        result = get_choice(
            "Select role:",
            ["admin", "customer"],
        )

    assert result == "customer"


def test_get_choice_invalid_then_valid():
    """Test invalid choice followed by valid choice."""

    with patch(
        "utils.input_helper.console.input",
        side_effect=["manager", "admin"],
    ):
        result = get_choice(
            "Select role:",
            ["admin", "customer"],
        )

    assert result == "admin"


def test_get_choice_empty_list():
    """Test that empty choices raise an error."""

    with pytest.raises(ValueError):
        get_choice("Select role:", [])


def test_get_yes_no_yes():
    """Test Yes response."""

    with patch(
        "utils.input_helper.console.input",
        return_value="y",
    ):
        result = get_yes_no("Continue?")

    assert result is True


def test_get_yes_no_no():
    """Test No response."""

    with patch(
        "utils.input_helper.console.input",
        return_value="n",
    ):
        result = get_yes_no("Continue?")

    assert result is False


def test_get_yes_no_invalid_then_valid():
    """Test invalid response followed by valid response."""

    with patch(
        "utils.input_helper.console.input",
        side_effect=["maybe", "yes"],
    ):
        result = get_yes_no("Continue?")

    assert result is True