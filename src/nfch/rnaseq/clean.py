"""Clean after a nfcore/rnaseq run."""

import typer

from nfch.file_manager import FileManager
from nfch.workflow import RNASeq

app = typer.Typer()


@app.command()
def clean() -> None:
    """Clean after a nfcore/rnaseq run is finished."""
    FileManager.clean(wf_folder=RNASeq.wf_folder)
