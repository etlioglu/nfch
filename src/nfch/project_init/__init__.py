import typer

from nfch.project_init.project_init import app as project_app

app = typer.Typer()

app.add_typer(typer_instance=project_app)
