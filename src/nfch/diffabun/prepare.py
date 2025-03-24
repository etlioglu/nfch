"""Creates a folder structure and associated command and settings files for nfcore/differentialabundance runs."""

from pathlib import Path
from typing import Annotated

import typer

from nfch import utils
from nfch.workflow import DiffAbun

app = typer.Typer()


@app.command()
def prepare(
    revision: Annotated[
        str,
        typer.Option(
            help="Pipeline version.",
        ),
    ] = "1.5.0",
    genome_build: Annotated[
        str,
        typer.Option(
            help="Genome build of interest.",
        ),
    ] = "GRCh38_Ensembl_release_113",
) -> None:
    """Create folders and files associated with a typical nfcore/differentialabundance run.

    Parameters
    ----------
    revision : Annotated[ str, typer.Option, optional
        Pipeline version, by default "3.18.0"
    genome_build : Annotated[ str, typer.Option, optional
        Genome build of interest, used to provide the right annotation for the "--gtf" parameter

    """
    diff_abun: DiffAbun = DiffAbun(revision=revision)
    diff_abun_dict: dict[str, str] = {"revision": diff_abun.revision, genome_build: "test"}

    settings_file: str = "diff_abun.json"
    utils.dict_to_json(dictionary=diff_abun_dict, file_path=Path(".nfch" / Path(settings_file)))
