"""Documentation to be added.

run from project directory's top level
uv run --active src/nfch/main.py --help

Resources:
https://sarahglasmacher.com/how-to-build-python-package-uv/
https://www.datacamp.com/tutorial/python-uv


Add --save_merged_fastq to the rnaseq nf_settings.json
"""

import typer

from nfch.diffabun import app as diffabun_app
from nfch.project_init import app as project_app
from nfch.rnaseq import app as rnaseq_app

app: typer.Typer = typer.Typer()

app.add_typer(typer_instance=project_app, name="project")
app.add_typer(typer_instance=rnaseq_app, name="rnaseq")
app.add_typer(typer_instance=diffabun_app, name="differentialabundance")


if __name__ == "__main__":
    app()
