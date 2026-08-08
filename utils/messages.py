"""
messages.py
------------
Centralized message utilities for PyCommerce.

Provides consistent success, error, warning, info,
and confirmation messages using Rich.
"""

from utils.console import console


def success(message: str):
    """Display a success message."""
    console.print(f"[bold green][SUCCESS][/bold green] {message}")


def error(message: str):
    """Display an error message."""
    console.print(f"[bold red][ERROR][/bold red] {message}")


def warning(message: str):
    """Display a warning message."""
    console.print(f"[bold yellow][WARNING][/bold yellow] {message}")


def info(message: str):
    """Display an informational message."""
    console.print(f"[bold cyan][INFO][/bold cyan] {message}")


def confirmation(message: str):
    """Display a confirmation message."""
    console.print(f"[bold blue][CONFIRMED][/bold blue] {message}")


def separator():
    """Display a visual separator."""
    console.print("[dim]" + "-" * 60 + "[/dim]")