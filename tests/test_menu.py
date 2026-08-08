from unittest.mock import patch

from utils.menu import Menu, MenuOption


def sample_action():
    """Sample menu action."""
    return None


def exit_action():
    """Sample exit action."""
    return True


def test_menu_creation():
    """Test menu creation."""

    menu = Menu("Main Menu")

    assert menu.title == "Main Menu"
    assert menu.options == []


def test_add_option():
    """Test adding menu options."""

    menu = Menu("Main Menu")

    menu.add_option(
        "Products",
        sample_action,
    )

    assert len(menu.options) == 1
    assert menu.options[0].number == 1
    assert menu.options[0].title == "Products"


def test_multiple_options():
    """Test multiple menu options."""

    menu = Menu("Main Menu")

    menu.add_option(
        "Products",
        sample_action,
    )

    menu.add_option(
        "Orders",
        sample_action,
    )

    assert len(menu.options) == 2
    assert menu.options[0].number == 1
    assert menu.options[1].number == 2


def test_menu_option_dataclass():
    """Test MenuOption."""

    option = MenuOption(
        number=1,
        title="Products",
        action=sample_action,
    )

    assert option.number == 1
    assert option.title == "Products"
    assert option.action == sample_action


def test_display():
    """Test menu display."""

    menu = Menu("Test Menu")

    menu.add_option(
        "Products",
        sample_action,
    )

    menu.display()


def test_get_selected_option():
    """Test option selection."""

    menu = Menu("Main Menu")

    menu.add_option(
        "Products",
        sample_action,
    )

    menu.add_option(
        "Orders",
        sample_action,
    )

    with patch(
        "utils.menu.get_integer",
        return_value=2,
    ):
        option = menu.get_selected_option()

    assert option.title == "Orders"


def test_execute_option():
    """Test executing a menu option."""

    called = []

    def action():
        called.append(True)

    menu = Menu("Main Menu")

    menu.add_option(
        "Test",
        action,
    )

    option = menu.options[0]

    menu.execute_option(option)

    assert called == [True]


def test_run_once():
    """Test running menu once."""

    called = []

    def action():
        called.append(True)

    menu = Menu("Main Menu")

    menu.add_option(
        "Test",
        action,
    )

    with patch(
        "utils.menu.get_integer",
        return_value=1,
    ):
        menu.run_once()

    assert called == [True]