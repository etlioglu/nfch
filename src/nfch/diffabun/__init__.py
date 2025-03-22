"""Presents the "diffabun" typer app."""

import typer

from nfch.diffabun.clean import app as clean_app
from nfch.diffabun.prepare import app as prepare_app

app = typer.Typer()

app.add_typer(typer_instance=prepare_app)
app.add_typer(typer_instance=clean_app)
