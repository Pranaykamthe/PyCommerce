"""
loading.py
----------
Loading and progress utilities for PyCommerce.

Provides reusable Rich loading indicators.
"""

from collections.abc import Callable
from typing import Any

from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)

from utils.console import console


def show_loading(
    message: str,
    function: Callable,
    *args,
    **kwargs,
) -> Any:
    """
    Execute a function while displaying a spinner.

    Args:
        message: Loading message.
        function: Function to execute.
        *args: Positional arguments for the function.
        **kwargs: Keyword arguments for the function.

    Returns:
        Result returned by the function.
    """

    with console.status(
        f"[bold cyan]{message}[/bold cyan]",
        spinner="dots",
    ):
        return function(*args, **kwargs)


def create_progress() -> Progress:
    """
    Create a reusable Rich progress bar.

    Returns:
        Configured Rich Progress object.
    """

    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
    )


def run_progress(
    description: str,
    total: int,
) -> Progress:
    """
    Create and start a progress display.

    Args:
        description: Description of the operation.
        total: Total number of steps.

    Returns:
        Active Progress object.
    """

    progress = create_progress()
    progress.start()

    progress.add_task(
        description,
        total=total,
    )

    return progress