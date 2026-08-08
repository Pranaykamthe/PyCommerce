from utils.ui import (
    show_banner,
    show_header,
    show_panel,
    show_welcome,
    show_goodbye,
)


def test_show_banner():
    """Test application banner."""
    show_banner()


def test_show_header():
    """Test page header."""
    show_header(
        "Products",
        "Manage your products."
    )


def test_show_panel():
    """Test generic panel."""
    show_panel(
        "Test Panel",
        "This is a test panel."
    )


def test_show_welcome():
    """Test welcome screen."""
    show_welcome()


def test_show_goodbye():
    """Test goodbye screen."""
    show_goodbye()