from utils.console import (
    console,
    clear_console,
    print_text,
    print_markup
)


def test_console_exists():
    """Test that the Rich console is created."""
    assert console is not None


def test_clear_console():
    """Test that clear_console executes successfully."""
    clear_console()


def test_print_text():
    """Test normal console output."""
    print_text("PyCommerce test")


def test_print_markup():
    """Test Rich markup output."""
    print_markup("[bold green]PyCommerce[/bold green]")