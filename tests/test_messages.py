from utils.messages import (
    success,
    error,
    warning,
    info,
    confirmation,
    separator
)


def test_success():
    """Test success message."""
    success("Operation completed successfully.")


def test_error():
    """Test error message."""
    error("Something went wrong.")


def test_warning():
    """Test warning message."""
    warning("This is a warning.")


def test_info():
    """Test informational message."""
    info("This is an information message.")


def test_confirmation():
    """Test confirmation message."""
    confirmation("Action confirmed.")


def test_separator():
    """Test separator output."""
    separator()