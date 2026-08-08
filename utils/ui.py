"""
ui.py
------
User interface utilities for PyCommerce.

Provides reusable Rich components such as:
- Application banner
- Page headers
- Panels
- Welcome screen
"""

from rich.align import Align
from rich.panel import Panel
from rich.text import Text

from utils.console import console


APP_NAME = "PyCommerce"
APP_VERSION = "1.0.0"


def show_banner():
    """Display the main PyCommerce application banner."""

    title = Text()
    title.append("PY", style="bold cyan")
    title.append("COMMERCE", style="bold white")

    subtitle = Text(
        f"E-Commerce Management System  |  Version {APP_VERSION}",
        style="dim",
    )

    content = Text()
    content.append(title)
    content.append("\n")
    content.append(subtitle)

    panel = Panel(
        Align.center(content),
        border_style="cyan",
        padding=(1, 4),
    )

    console.print(panel)


def show_header(title: str, subtitle: str | None = None):
    """
    Display a page/section header.

    Args:
        title: Main header title.
        subtitle: Optional description below the title.
    """

    content = Text()
    content.append(title, style="bold cyan")

    if subtitle:
        content.append(f"\n{subtitle}", style="dim")

    panel = Panel(
        content,
        border_style="blue",
        padding=(0, 2),
    )

    console.print(panel)


def show_panel(
    title: str,
    content: str,
    border_style: str = "cyan",
):
    """
    Display a generic information panel.

    Args:
        title: Panel title.
        content: Panel content.
        border_style: Rich border style/color.
    """

    panel = Panel(
        content,
        title=title,
        border_style=border_style,
        padding=(1, 2),
    )

    console.print(panel)


def show_welcome():
    """Display the PyCommerce welcome screen."""

    show_banner()

    console.print()

    show_panel(
        "Welcome",
        "Welcome to PyCommerce!\n"
        "Your console-based e-commerce management system.",
        border_style="green",
    )


def show_goodbye():
    """Display the application exit message."""

    show_panel(
        "Goodbye",
        "Thank you for using PyCommerce!",
        border_style="yellow",
    )