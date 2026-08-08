"""
menu.py
-------
Reusable menu utilities for PyCommerce.

Provides a generic menu system that can be reused
for customer, admin, product, cart, and order menus.
"""

from dataclasses import dataclass
from typing import Callable

from rich.table import Table

from utils.console import console
from utils.input_helper import get_integer


@dataclass
class MenuOption:
    """
    Represents a single menu option.

    Attributes:
        number: Option number.
        title: Text displayed to the user.
        action: Function executed when selected.
    """

    number: int
    title: str
    action: Callable


class Menu:
    """
    Reusable interactive menu.

    Example:

        menu = Menu("Main Menu")

        menu.add_option(
            "Products",
            show_products
        )

        menu.add_option(
            "Exit",
            exit_application
        )

        menu.run()
    """

    def __init__(self, title: str):
        """
        Initialize a menu.

        Args:
            title: Menu title.
        """

        self.title = title
        self.options: list[MenuOption] = []

    def add_option(
        self,
        title: str,
        action: Callable,
    ):
        """
        Add an option to the menu.

        Args:
            title: Option title.
            action: Function executed when selected.
        """

        number = len(self.options) + 1

        option = MenuOption(
            number=number,
            title=title,
            action=action,
        )

        self.options.append(option)

    def display(self):
        """Display the menu."""

        table = Table(
            title=self.title,
            show_header=True,
            header_style="bold cyan",
            border_style="blue",
        )

        table.add_column(
            "Option",
            justify="center",
            style="bold yellow",
        )

        table.add_column(
            "Action",
            style="white",
        )

        for option in self.options:
            table.add_row(
                str(option.number),
                option.title,
            )

        console.print(table)

    def get_selected_option(self) -> MenuOption:
        """
        Ask the user to select an option.

        Returns:
            Selected MenuOption.
        """

        choice = get_integer(
            "Select an option",
            min_value=1,
            max_value=len(self.options),
        )

        return self.options[choice - 1]

    def execute_option(self, option: MenuOption):
        """
        Execute a selected menu option.

        Args:
            option: MenuOption to execute.
        """

        option.action()

    def run_once(self):
        """Display and execute the menu once."""

        self.display()

        option = self.get_selected_option()

        self.execute_option(option)

    def run(self):
        """
        Continuously run the menu.

        The menu stops when an action returns True.
        """

        while True:
            self.display()

            option = self.get_selected_option()

            result = option.action()

            if result is True:
                break