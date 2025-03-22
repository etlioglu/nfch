"""Module contatining the class FileManager managing file/folder operations."""

import shutil
import sys
from pathlib import Path

from nfch import utils


class FileManager:
    """A class for file/folder operations."""

    @staticmethod
    def clean(wf_folder: Path) -> None:
        """Clean after a nfcore run.

        Parameters
        ----------
        wf_folder : Path
            _Folder "work" containing all intermediate/final files/folders for a nfcore run

        """
        run_folder: Path = wf_folder / "run" / "work"
        try:
            utils.processing(message=f'Removing "{run_folder}"...')
            shutil.rmtree(path=run_folder)
            utils.success(message=f'"{run_folder}" has been removed successfully.')
        except FileNotFoundError:
            utils.fail(message=f'Folder "{run_folder}" could not be found, exiting!')
            sys.exit()
