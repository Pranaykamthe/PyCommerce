"""
input_helper.py
---------------
Reusable input utilities for PyCommerce.

Provides safe functions for:
- Text input
- Integer input
- Decimal input
- Choice input
- Yes/No input
"""

from decimal import Decimal, InvalidOperation

from utils.console import console


def get_text(prompt: str, allow_empty: bool = False) -> str:
    """
    Get text input from the user.

    Args:
        prompt: Message displayed to the user.
        allow_empty: Whether an empty value is allowed.

    Returns:
        User-entered text.
    """

    while True:
        value = console.input(f"[bold cyan]{prompt}[/bold cyan] ").strip()

        if value or allow_empty:
            return value

        console.print(
            "[bold red]Input cannot be empty.[/bold red]"
        )


def get_integer(
    prompt: str,
    min_value: int | None = None,
    max_value: int | None = None,
) -> int:
    """
    Get a valid integer from the user.

    Args:
        prompt: Message displayed to the user.
        min_value: Optional minimum allowed value.
        max_value: Optional maximum allowed value.

    Returns:
        Valid integer.
    """

    while True:
        value = console.input(
            f"[bold cyan]{prompt}[/bold cyan] "
        ).strip()

        try:
            number = int(value)

            if min_value is not None and number < min_value:
                console.print(
                    f"[bold red]Value must be at least "
                    f"{min_value}.[/bold red]"
                )
                continue

            if max_value is not None and number > max_value:
                console.print(
                    f"[bold red]Value must not exceed "
                    f"{max_value}.[/bold red]"
                )
                continue

            return number

        except ValueError:
            console.print(
                "[bold red]Please enter a valid integer.[/bold red]"
            )


def get_decimal(
    prompt: str,
    min_value: Decimal | None = None,
    max_value: Decimal | None = None,
) -> Decimal:
    """
    Get a valid decimal number from the user.

    Args:
        prompt: Message displayed to the user.
        min_value: Optional minimum allowed value.
        max_value: Optional maximum allowed value.

    Returns:
        Valid Decimal value.
    """

    while True:
        value = console.input(
            f"[bold cyan]{prompt}[/bold cyan] "
        ).strip()

        try:
            number = Decimal(value)

            if min_value is not None and number < min_value:
                console.print(
                    f"[bold red]Value must be at least "
                    f"{min_value}.[/bold red]"
                )
                continue

            if max_value is not None and number > max_value:
                console.print(
                    f"[bold red]Value must not exceed "
                    f"{max_value}.[/bold red]"
                )
                continue

            return number

        except InvalidOperation:
            console.print(
                "[bold red]Please enter a valid number.[/bold red]"
            )


def get_choice(
    prompt: str,
    choices: list[str],
) -> str:
    """
    Get a valid choice from a list.

    Args:
        prompt: Message displayed to the user.
        choices: List of valid choices.

    Returns:
        Selected choice.
    """

    if not choices:
        raise ValueError("Choices cannot be empty.")

    while True:
        value = console.input(
            f"[bold cyan]{prompt}[/bold cyan] "
        ).strip()

        for choice in choices:
            if value.lower() == choice.lower():
                return choice

        console.print(
            "[bold red]Invalid choice. "
            f"Choose from: {', '.join(choices)}[/bold red]"
        )


def get_yes_no(prompt: str) -> bool:
    """
    Get a Yes/No answer from the user.

    Args:
        prompt: Message displayed to the user.

    Returns:
        True for yes, False for no.
    """

    while True:
        value = console.input(
            f"[bold cyan]{prompt} (y/n):[/bold cyan] "
        ).strip().lower()

        if value in ("y", "yes"):
            return True

        if value in ("n", "no"):
            return False

        console.print(
            "[bold red]Please enter Y/Yes or N/No.[/bold red]"
        )