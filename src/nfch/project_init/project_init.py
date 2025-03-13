"""Initiates a project that will be using nfcore pipelines."""

from pathlib import Path
from typing import Annotated

import typer

from nfch import utils
from nfch.proj import Project

app = typer.Typer()


@app.command()
def prerequisites() -> None:
    """Show prerequisites of a typical nfcore project."""
    one = """
    1- Run this tool from within the top level directory of your project.
    """
    utils.info(message=one)

    two = """
    2- It is advised that the aforementioned top level directory is under version control for reproducibility purposes.
    """
    utils.info(message=two)

    three = """
    3- Initiation of the project is accomplished via the command "nfch project init" and it expects an optional
    parameter "genomes.json", listing available genomes. If not supplied, you will need to manually enter this
    information in the"nf_params.json" file once created by this tool.
    """
    utils.info(message=three)

    extras = """
    Extra things to check:
    1- Teams channel
    2- git repo
    3- secuing raw data after checksum
    4- meta data to the Teams channel
    """
    utils.info(message=extras)


@app.command()
def init(
    email: Annotated[
        str | None,
        typer.Option(
            help="E-mail address to receive information regarding Nextflow runs.",
        ),
    ] = None,
    genomes_json: Annotated[
        Path | None,
        typer.Option(help="Path to the json file containing genome information."),
    ] = None,
) -> None:
    """Initiate project, track user, available genomes, ..."""
    Project(email=email, genomes_json=genomes_json)


@app.command()
def show_settings() -> None:
    """Show project settings: user, available genomes, ..."""
