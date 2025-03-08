"""The module contains some utility functions used by all the submodules."""

import json
import textwrap
from pathlib import Path

from rich import print as rich_print


def json_to_dict(file: Path) -> dict[str, str]:
    """Convert a json file to a dict.

    Parameters
    ----------
    file : Path
        file path

    Returns
    -------
    dict[str, str]
        dict

    """
    with Path.open(self=file, encoding="utf-8") as json_file:
        data: dict[str, str] = json.load(fp=json_file)
    return data


def dict_to_json(dictionary: dict[str, str], file: Path) -> None:
    """Write a dict into a json file.

    Parameters
    ----------
    dictionary : dict[str, str]
        dict
    file : Path
        file path

    """
    with Path.open(self=file, mode="w", encoding="utf-8") as json_file:
        json.dump(obj=dictionary, fp=json_file, indent=2)


def _format_message(message: str) -> str:
    """Format messages.

    "textwrap.dedent" is used for strings with triple quotes and "str.strip()"
    removes leading and trailing new lines (technically all whitespaces).

    Parameters
    ----------
    message : str
        message to be printed

    Returns
    -------
    str
        formatted message

    """
    return str.strip(textwrap.dedent(message))


def processing(message: str) -> None:
    """Print formatted message.

    Parameters
    ----------
    message : str
        str

    """
    rich_print(f"\n[blue]{_format_message(message)}[blue]")


def success(message: str) -> None:
    """Print formatted message.

    Parameters
    ----------
    message : str
        str

    """
    rich_print(f"\n[green]{_format_message(message)}[green]")


def warning(message: str) -> None:
    """Print formatted message.

    Parameters
    ----------
    message : str
        str

    """
    rich_print(f"\n[orange1]{_format_message(message)}[orange1]")


def fail(message: str) -> None:
    """Print formatted message.

    Parameters
    ----------
    message : str
        str

    """
    rich_print(f"\n[red]{_format_message(message)}[red]")


def info(message: str) -> None:
    """Print formatted message.

    Parameters
    ----------
    message : str
        str

    """
    rich_print(f"\n[yellow]{_format_message(message)}[yellow]")
