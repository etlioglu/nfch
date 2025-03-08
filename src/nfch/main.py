"""Documentation to be added.

/home/eetlioglu/analyses/emre-etlioglu/nfch/src/nfch
uv run --active main.py --help

TODO: Configure ruff: https://docs.astral.sh/ruff/configuration/
TODO add pre-commit hooks
"""

import typer
from project_init.project_init import app as project_app

# from nfch.rnaseq import app as rnaseq_app
# from nfch.diffab import app as diffab_app

app: typer.Typer = typer.Typer()

app.add_typer(typer_instance=project_app, name="project")
# app.add_typer(rnaseq_app:typer.Typer, name="rnaseq")
# app.add_typer(diffab, name="differentialabundance")


if __name__ == "__main__":
    app()
