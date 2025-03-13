"""The module contains some utility functions used by all the submodules."""

import json
import sys
import textwrap
from pathlib import Path
from typing import Any

from rich import print as rich_print


def dict_to_json(dictionary: dict[str, Any], file_path: Path) -> None:
    """Write a dict into a json file.

    Parameters
    ----------
    dictionary : dict[str, str]
        dict
    file_path : Path
        File path

    """
    try:
        with file_path.open(mode="w", encoding="utf-8") as json_file:
            json.dump(obj=dictionary, fp=json_file, indent=2)
    except PermissionError:
        fail(message=f'"{file_path}" is not writable, aborting!')
        sys.exit()


def json_to_dict(file_path: Path) -> dict[str, Any]:
    """Convert a json file to a dict.

    Parameters
    ----------
    file_path : Path
        File path

    Returns
    -------
    dict[str, str]
        dict

    """
    try:
        with file_path.open(mode="r", encoding="utf-8") as json_file:
            data: dict[str, Any] = json.load(fp=json_file)
    except FileNotFoundError:
        fail(message=f'File "{file_path}" not found, aborting!')
        sys.exit()
    return data


def _format_message(message: str) -> str:
    """Format messages.

    "textwrap.dedent" is used for strings with triple quotes and "str.strip()" removes leading and trailing new lines
    (technically all whitespaces).

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


def create_folder(folder_path: Path) -> None:
    """Create a folder.

    Parameters
    ----------
    folder_path : Path
        Path to the folder of interest

    """
    try:
        folder_path.mkdir()
        success(message=f'Directory "{folder_path}" created successfully.')
    except FileExistsError:
        fail(
            message=f'Directory "{folder_path}" already exists, aborting! You can remove or rename "{folder_path}"'
            "and try again.",
        )
        sys.exit()
    except PermissionError:
        fail(message=f'Directory "{folder_path.parent}" is not writable, aborting!')
        sys.exit()


def string_to_textfile(text: str, file_path: Path) -> None:
    """Write a string to a text file.

    Parameters
    ----------
    text : str
        Text
    file_path : Path
        File path

    """
    try:
        with file_path.open(mode="w", encoding="utf-8") as text_file:
            text_file.write(text)
    except PermissionError:
        fail(message=f'"{file_path}" is not writable, aborting!')
        sys.exit()
    success(message=f'File "{file_path}" has been created successfully.')
