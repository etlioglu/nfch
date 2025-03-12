"""Utiliy functions for project initiation."""

import shutil
import sys
from pathlib import Path

from nfch import utils


def under_version_control() -> bool:
    """Check if the working/project directory is under version control.

    Returns
    -------
    bool
        True/False

    """
    git_folder: Path = Path(".git")
    if git_folder.is_dir():
        utils.success(message="The project folder seems to be under git version control.")
        return True
    utils.warning(
        message="The project folder does not seem to be under revision control, this is advised for repoducibility"
        "but not forced.",
    )
    return False


def create_settings_folder() -> None:
    """Create a settings folder, ".nfch", within the project directory (if not present) and store settings there."""
    settings_folder: Path = Path(".nfch")

    # check if the folder is really a folder and not a file
    if settings_folder.exists():
        if settings_folder.is_dir():
            utils.warning(message=f'Folder "{settings_folder}" already exists.')
        else:
            utils.fail(message=f'"{settings_folder}" exists but is not a folder!')
            sys.exit()  # exit the program
    else:
        try:
            settings_folder.mkdir()
        except PermissionError:
            utils.fail(message=f'"{settings_folder.parent}" is not writable!')
            sys.exit()
        utils.success(message=f'Folder "{settings_folder}" has been created.')


def create_settings_file(email: str | None = None) -> None:
    """Create a settings folder, ".nfch", within the project directory (if not present) and store settings there.

    Parameters
    ----------
    email : str | None
        E-mail address of the user

    """
    # a dict is used in case new setting types other than e-mail will be introduced in the future
    new_settings: dict[str, str] = {}
    if email:
        new_settings["email"] = email

    # settings
    settings_file: Path = Path(".nfch/settings.json")
    if settings_file.exists():
        utils.warning(
            message=f'File "{settings_file}" already exists, information provided with "nfch project init" will'
            "be added to this file if not already present or will be overridden otherwise!"
            'Tip: "nfch project settings" will show existing information about the current project.',
        )

        old_settings: dict[str, str] = utils.json_to_dict(
            file=settings_file,
        )
        old_settings.update(new_settings)
        utils.dict_to_json(
            dictionary=old_settings,
            file=settings_file,
        )
    else:
        utils.processing(
            message=f"Creating {settings_file}...",
        )
        utils.dict_to_json(
            dictionary=new_settings,
            file=settings_file,
        )


def _genome_paths_ok(genomes_json: Path) -> bool:
    """Check if the paths to the genome files are valid.

    Parameters
    ----------
    genomes_json : Path
        Path to the json file containing genome information

    Returns
    -------
    bool
        True/False

    """
    genomes_dict: dict[str, dict[str, str]] = utils.json_to_dict(file=genomes_json)
    for genome_build, paths in genomes_dict.items():
        for file_type, file_path in paths.items():
            if file_path and Path(file_path).exists():
                pass
            elif not file_path:
                utils.warning(message=f'"{file_type}" path for {genome_build} is missing.')
            else:
                utils.fail(message=f'"{file_path}" does not seem to be a valid path for {file_type} of {genome_build}!')
                return False
    utils.success("All existing paths within the genomes.json are valid.")
    return True


def copy_genomes_json(genomes_json: str) -> None:
    """Copy the genomes.json file to the ".nfch/" folder.

    Parameters
    ----------
    genomes_json : str
        Path to the json file storing genome information

    """
    genomes_json_src_path: Path = Path(genomes_json)
    if not genomes_json_src_path.exists():
        utils.fail(message=f'"{genomes_json_src_path}" does not seem to be a valid path!')
    elif not _genome_paths_ok(genomes_json=genomes_json_src_path):
        utils.fail(message='At least one of the paths within the "genomes.json" is not valid!')
    else:
        genomes_json_dst_path: Path = Path(".nfch/genomes.json")
        if genomes_json_dst_path.exists():
            utils.warning(message=f'"{genomes_json_dst_path}" exists already and will be overwritten!')
        utils.processing(
            message=f'"{genomes_json_src_path}" is being copied into "{genomes_json_dst_path.parent}/"...',
        )
        shutil.copy(src=genomes_json_src_path, dst=genomes_json_dst_path)
