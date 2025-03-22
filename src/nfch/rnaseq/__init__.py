"""Presents the "rnaseq" typer app serving as the "rnaseq sub-command" to take care of managing nfcore/rnaseq runs."""

import typer

from nfch.rnaseq.clean import app as clean_app

# from nfch.rnaseq.extract import app as extract_app
from nfch.rnaseq.prepare import app as prepare_app

app = typer.Typer()

app.add_typer(typer_instance=prepare_app)
app.add_typer(typer_instance=clean_app)
# app.add_typer(typer_instance=extract_app)
