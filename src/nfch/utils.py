"""The module contains some utility functions used by all the submodules."""

import json
import sys
from pathlib import Path
from typing import Any

from nfch.message_manager import MessageManager


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
        MessageManager.fail(message=f'"{file_path}" is not writable, aborting!')
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
        MessageManager.fail(message=f'File "{file_path}" not found, aborting!')
        sys.exit()
    return data


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
        MessageManager.fail(message=f'"{file_path}" is not writable, aborting!')
        sys.exit()
    MessageManager.success(message=f'File "{file_path}" has been created successfully.')

    def create_folder(folder_path: Path) -> None:
        """Create a folder.

        Parameters
        ----------
        folder_path : Path
            Path to the folder of interest

        """
        try:
            folder_path.mkdir()
            MessageManager.success(message=f'Directory "{folder_path}" created successfully.')
        except FileExistsError:
            MessageManager.fail(
                message=f'Directory "{folder_path}" already exists, aborting! You can remove or rename "{folder_path}"'
                "and try again.",
            )
            sys.exit()
        except PermissionError:
            MessageManager.fail(message=f'Directory "{folder_path.parent}" is not writable, aborting!')
            sys.exit()
