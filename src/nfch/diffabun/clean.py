"""Clean after a nfcore/rnaseq run."""

import typer

from nfch.file_manager import FileManager
from nfch.workflow import DiffAbun

app = typer.Typer()


@app.command()
def clean() -> None:
    """Clean after a nfcore/differentialabundance run is finished."""
    FileManager.clean(wf_folder=DiffAbun.wf_folder)
