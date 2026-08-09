"""
Integration tests for Wishlist UI.
"""

from unittest.mock import patch

from models.wishlist import Wishlist

from ui import wishlist_ui


# ============================================================
# DISPLAY WISHLIST
# ============================================================

def test_display_wishlist_empty():
    """Test displaying an empty wishlist."""

    wishlist_ui.display_wishlist([])


def test_display_wishlist_with_items():
    """Test displaying wishlist items."""

    items = [
        Wishlist(
            wishlist_id=1,
            user_id=1,
            product_id=10
        ),
        Wishlist(
            wishlist_id=2,
            user_id=1,
            product_id=20
        )
    ]

    wishlist_ui.display_wishlist(
        items
    )


# ============================================================
# VIEW WISHLIST
# ============================================================

def test_view_wishlist():
    """Test viewing a user's wishlist."""

    items = [
        Wishlist(
            wishlist_id=1,
            user_id=1,
            product_id=10
        )
    ]

    with patch(
        "ui.wishlist_ui.WishlistService.get_wishlist",
        return_value=items
    ):

        result = wishlist_ui.view_wishlist(
            1
        )

    assert result == items


def test_view_wishlist_empty():
    """Test viewing an empty wishlist."""

    with patch(
        "ui.wishlist_ui.WishlistService.get_wishlist",
        return_value=[]
    ):

        result = wishlist_ui.view_wishlist(
            1
        )

    assert result == []


def test_view_wishlist_error():
    """Test wishlist view when service raises ValueError."""

    with patch(
        "ui.wishlist_ui.WishlistService.get_wishlist",
        side_effect=ValueError(
            "Invalid user ID."
        )
    ):

        result = wishlist_ui.view_wishlist(
            0
        )

    assert result == []


# ============================================================
# ADD TO WISHLIST
# ============================================================

def test_add_to_wishlist_success():
    """Test adding a product to the wishlist."""

    with patch(
        "builtins.input",
        return_value="10"
    ), patch(
        "ui.wishlist_ui.WishlistService.add_to_wishlist",
        return_value=True
    ) as mock_add:

        result = wishlist_ui.add_to_wishlist(
            1
        )

    assert result is True

    mock_add.assert_called_once_with(
        user_id=1,
        product_id=10
    )


def test_add_to_wishlist_failure():
    """Test failed wishlist addition."""

    with patch(
        "builtins.input",
        return_value="10"
    ), patch(
        "ui.wishlist_ui.WishlistService.add_to_wishlist",
        return_value=False
    ):

        result = wishlist_ui.add_to_wishlist(
            1
        )

    assert result is False


def test_add_to_wishlist_value_error():
    """Test invalid wishlist addition."""

    with patch(
        "builtins.input",
        return_value="10"
    ), patch(
        "ui.wishlist_ui.WishlistService.add_to_wishlist",
        side_effect=ValueError(
            "Product is already in the wishlist."
        )
    ):

        result = wishlist_ui.add_to_wishlist(
            1
        )

    assert result is False


def test_add_to_wishlist_invalid_input():
    """Test non-numeric product ID."""

    with patch(
        "builtins.input",
        return_value="abc"
    ):

        result = wishlist_ui.add_to_wishlist(
            1
        )

    assert result is False


# ============================================================
# REMOVE FROM WISHLIST
# ============================================================

def test_remove_from_wishlist_success():
    """Test removing a product from wishlist."""

    with patch(
        "builtins.input",
        return_value="10"
    ), patch(
        "ui.wishlist_ui.WishlistService.remove_from_wishlist",
        return_value=True
    ) as mock_remove:

        result = wishlist_ui.remove_from_wishlist(
            1
        )

    assert result is True

    mock_remove.assert_called_once_with(
        user_id=1,
        product_id=10
    )


def test_remove_from_wishlist_failure():
    """Test failed wishlist removal."""

    with patch(
        "builtins.input",
        return_value="10"
    ), patch(
        "ui.wishlist_ui.WishlistService.remove_from_wishlist",
        return_value=False
    ):

        result = wishlist_ui.remove_from_wishlist(
            1
        )

    assert result is False


def test_remove_from_wishlist_value_error():
    """Test removing a product not in wishlist."""

    with patch(
        "builtins.input",
        return_value="10"
    ), patch(
        "ui.wishlist_ui.WishlistService.remove_from_wishlist",
        side_effect=ValueError(
            "Product is not in the wishlist."
        )
    ):

        result = wishlist_ui.remove_from_wishlist(
            1
        )

    assert result is False


def test_remove_from_wishlist_invalid_input():
    """Test non-numeric product ID."""

    with patch(
        "builtins.input",
        return_value="abc"
    ):

        result = wishlist_ui.remove_from_wishlist(
            1
        )

    assert result is False


# ============================================================
# CLEAR WISHLIST
# ============================================================

def test_clear_wishlist_success():
    """Test successfully clearing wishlist."""

    with patch(
        "builtins.input",
        return_value="y"
    ), patch(
        "ui.wishlist_ui.WishlistService.clear_wishlist",
        return_value=True
    ) as mock_clear:

        result = wishlist_ui.clear_wishlist(
            1
        )

    assert result is True

    mock_clear.assert_called_once_with(
        1
    )


def test_clear_wishlist_empty():
    """Test clearing an empty wishlist."""

    with patch(
        "builtins.input",
        return_value="y"
    ), patch(
        "ui.wishlist_ui.WishlistService.clear_wishlist",
        return_value=False
    ):

        result = wishlist_ui.clear_wishlist(
            1
        )

    assert result is False


def test_clear_wishlist_cancelled():
    """Test cancelling wishlist clearing."""

    with patch(
        "builtins.input",
        return_value="n"
    ):

        result = wishlist_ui.clear_wishlist(
            1
        )

    assert result is False


def test_clear_wishlist_error():
    """Test clearing wishlist when service raises an error."""

    with patch(
        "builtins.input",
        return_value="y"
    ), patch(
        "ui.wishlist_ui.WishlistService.clear_wishlist",
        side_effect=ValueError(
            "Invalid user ID."
        )
    ):

        result = wishlist_ui.clear_wishlist(
            0
        )

    assert result is False


# ============================================================
# WISHLIST MENU
# ============================================================

def test_wishlist_menu_back():
    """Test returning from wishlist menu."""

    with patch(
        "builtins.input",
        return_value="0"
    ):

        wishlist_ui.wishlist_menu(
            1
        )


def test_wishlist_menu_view():
    """Test wishlist menu view option."""

    with patch(
        "builtins.input",
        side_effect=["1", "0"]
    ), patch(
        "ui.wishlist_ui.view_wishlist"
    ) as mock_view:

        wishlist_ui.wishlist_menu(
            1
        )

    mock_view.assert_called_once_with(
        1
    )


def test_wishlist_menu_add():
    """Test wishlist menu add option."""

    with patch(
        "builtins.input",
        side_effect=["2", "0"]
    ), patch(
        "ui.wishlist_ui.add_to_wishlist"
    ) as mock_add:

        wishlist_ui.wishlist_menu(
            1
        )

    mock_add.assert_called_once_with(
        1
    )


def test_wishlist_menu_remove():
    """Test wishlist menu remove option."""

    with patch(
        "builtins.input",
        side_effect=["3", "0"]
    ), patch(
        "ui.wishlist_ui.remove_from_wishlist"
    ) as mock_remove:

        wishlist_ui.wishlist_menu(
            1
        )

    mock_remove.assert_called_once_with(
        1
    )


def test_wishlist_menu_clear():
    """Test wishlist menu clear option."""

    with patch(
        "builtins.input",
        side_effect=["4", "0"]
    ), patch(
        "ui.wishlist_ui.clear_wishlist"
    ) as mock_clear:

        wishlist_ui.wishlist_menu(
            1
        )

    mock_clear.assert_called_once_with(
        1
    )


def test_wishlist_menu_invalid_choice():
    """Test invalid wishlist menu choice."""

    with patch(
        "builtins.input",
        side_effect=["99", "0"]
    ):

        wishlist_ui.wishlist_menu(
            1
        )