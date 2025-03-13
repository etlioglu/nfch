"""Creates a folder structure and associated command and settings files for nfcore/rnaseq runs."""

from typing import Annotated

import typer
from workflow import RNASeq

app = typer.Typer()


@app.command()
def prepare(
    revision: Annotated[
        str,
        typer.Option(
            help="Pipeline version.",
        ),
    ] = "3.18.0",
    genome_build: Annotated[
        str,
        typer.Option(
            help="Genome build of interest.",
        ),
    ] = "GRCh38_Ensembl_release_113",
) -> None:
    """Create folders and files associated with a typical nfcore/rnaseq run.

    Parameters
    ----------
    revision : Annotated[ str, typer.Option, optional
        Pipeline version, by default "3.18.0"
    genome_build : Annotated[ str, typer.Option, optional
        Genome build of interest, must match one of the keys in the "genomes.json file", by default
        "GRCh38_Ensembl_release_113"

    """
    RNASeq(name="nfcore_rnaseq", revision=revision, genome_build=genome_build)
