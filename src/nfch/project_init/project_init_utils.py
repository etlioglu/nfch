"""Utiliy functions for project initiation."""

import shutil
from pathlib import Path

from nfch import utils


def under_version_control() -> bool:
    """Check if the working directory is under version control.

    Returns
    -------
    bool
        True/False

    """
    git_folder: Path = Path(".git")
    if git_folder.is_dir():
        utils.success(
            message="The project folder seems to be under git version control",
        )
        return True
    utils.warning(
        message="The project folder does not seem to be under revision control, this is advised but not forced",
    )
    return False


def create_settings(
    email: str | None = None,
    genomes_json: str | None = None,
) -> None:
    """Create a settings folder, ".nfch", within the project directory (if not present) and store settings there.

    Parameters
    ----------
    email : str | None
        E-mail address of the user
    genomes_json : str | None
        Path to the json file storing genome information

    """
    settings_folder: Path = Path(".nfch")

    try:
        settings_folder.mkdir()
    except FileExistsError:
        utils.warning(
            message=f'Folder "{settings_folder}" already exists.',
        )

    # a dict is used in case new setting types will be introduced in the future
    new_settings: dict[str, str] = {}
    if email:
        new_settings["email"] = email

    # settings
    settings_file: Path = settings_folder / "nfch_settings.json"
    if settings_file.exists():
        long_message: str = f"""
        File "{settings_file}" already exists, information provided with "nfch project init" will be added if not
        already present within that file or will be overridden otherwise!
        Tip: "nfch project settings" will show existing information about the current project.
        """
        utils.warning(message=long_message)
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

    # json file containing genome related info: fasta, gtf, index
    if genomes_json:
        genomes_json_src_path: Path = Path(genomes_json)
        if not genomes_json_src_path.exists():
            utils.fail(
                message=f'"{genomes_json_src_path}" does not seem to be a valid path!',
            )
        else:
            genomes_json_dst_path: Path = settings_folder / "genomes.json"
            if genomes_json_dst_path.exists():
                utils.warning(message=f'"{genomes_json_dst_path}" exists already and will be overwritten!')
            utils.processing(
                message=f'"{genomes_json_src_path}" is being copied into "{genomes_json_dst_path.parent}"...',
            )
            shutil.copy(
                src=genomes_json_src_path,
                dst=genomes_json_dst_path,
            )
