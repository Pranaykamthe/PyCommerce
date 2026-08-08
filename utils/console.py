"""
console.py
-----------
Central Rich console configuration for PyCommerce.

This module provides a single Console instance that can be
used throughout the application.
"""

from rich.console import Console


console = Console()


def clear_console():
    """Clear the terminal screen."""
    console.clear()


def print_text(message: str):
    """Print normal text to the console."""
    console.print(message)


def print_markup(message: str):
    """Print Rich-formatted markup."""
    console.print(message, markup=True)