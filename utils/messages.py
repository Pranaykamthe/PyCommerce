"""
messages.py
------------
Centralized message utilities for PyCommerce.

Provides consistent success, error, warning, info,
and confirmation messages using Rich.
"""

from utils.console import console


def success(message: str) -> None:
    """Display a success message."""
    console.print(
        f"[bold green][SUCCESS][/bold green] {message}"
    )


def error(message: str) -> None:
    """Display an error message."""
    console.print(
        f"[bold red][ERROR][/bold red] {message}"
    )


def warning(message: str) -> None:
    """Display a warning message."""
    console.print(
        f"[bold yellow][WARNING][/bold yellow] {message}"
    )


def info(message: str) -> None:
    """Display an informational message."""
    console.print(
        f"[bold cyan][INFO][/bold cyan] {message}"
    )


def confirmation(message: str) -> None:
    """Display a confirmation message."""
    console.print(
        f"[bold blue][CONFIRMED][/bold blue] {message}"
    )


def separator() -> None:
    """Display a visual separator."""
    console.print(
        "[dim]" + "-" * 60 + "[/dim]"
    )


# ==========================================
# show_* aliases for UI integration
# ==========================================

def show_success(message: str) -> None:
    """Display a success message."""
    success(message)


def show_error(message: str) -> None:
    """Display an error message."""
    error(message)


def show_warning(message: str) -> None:
    """Display a warning message."""
    warning(message)


def show_info(message: str) -> None:
    """Display an informational message."""
    info(message)


def show_confirmation(message: str) -> None:
    """Display a confirmation message."""
    confirmation(message)


def show_separator() -> None:
    """Display a visual separator."""
    separator()