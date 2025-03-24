"""Module contatining the class MessageManager managing colored output messages."""

import textwrap

from rich import print as rich_print


class MessageManager:
    """A utility class for printing colored messages."""

    @staticmethod
    def _format_message(message: str) -> str:
        """Format messages.

        "textwrap.dedent" is used for strings with triple quotes and "str.strip()" removes leading and trailing new
        lines (technically all whitespaces).

        Parameters
        ----------
        message : str
            message to be printed

        Returns
        -------
        str
            formatted message

        """
        return str.strip(textwrap.dedent(text=message))

    @staticmethod
    def processing(message: str) -> None:
        """Print formatted message.

        Parameters
        ----------
        message : str
            str

        """
        rich_print(f"\n[blue]{MessageManager._format_message(message=message)}[blue]")

    @staticmethod
    def success(message: str) -> None:
        """Print formatted message.

        Parameters
        ----------
        message : str
            str

        """
        rich_print(f"\n[green]{MessageManager._format_message(message=message)}[green]")

    @staticmethod
    def warning(message: str) -> None:
        """Print formatted message.

        Parameters
        ----------
        message : str
            str

        """
        rich_print(f"\n[orange1]{MessageManager._format_message(message=message)}[orange1]")

    @staticmethod
    def fail(message: str) -> None:
        """Print formatted message.

        Parameters
        ----------
        message : str
            str

        """
        rich_print(f"\n[red]{MessageManager._format_message(message=message)}[red]")

    @staticmethod
    def info(message: str) -> None:
        """Print formatted message.

        Parameters
        ----------
        message : str
            str

        """
        rich_print(f"\n[yellow]{MessageManager._format_message(message=message)}[yellow]")
