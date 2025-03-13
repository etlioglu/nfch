"""Classes representing nfcore workflows."""

import textwrap
from pathlib import Path

import utils


class Workflow:
    """A class representing generic workflows."""

    # Add the clean functionality

    def __init__(self, name: str) -> None:
        """Instantiate the generic Workflow object and create the necessary folders.

        Parameters
        ----------
        name : str
            nfcore workflow name

        """
        self.name: str = name
        self.wf_folder: Path = Path(name)
        self.metadata_folder: Path = self.wf_folder / "metadata"
        self.run_folder: Path = self.wf_folder / "run"
        self.output_folder: Path = self.wf_folder / "output"
        self.nf_settings: Path = self.run_folder / "nf_params.json"

        # create folder for the workflow of interest
        utils.create_folder(folder_path=self.wf_folder)

        # create subfolder for metadata: sample sheet, contrast sheet, etc.
        utils.create_folder(folder_path=self.metadata_folder)

        # create subfolder for the run: Nextflow command, settings, etc.
        utils.create_folder(folder_path=self.run_folder)

        # create subfolder for the output
        utils.create_folder(folder_path=self.output_folder)


class RNASeq(Workflow):
    """A class representing nfcore/rnaseq workflows."""

    def __init__(self, name: str, revision: str, genome_build: str) -> None:
        """Instantiate the RNASeq object and create the nfcore/rnaseq specific command and settings files.

        Parameters
        ----------
        name : str
            Workflow name, used by the parent class' init method
        revision : str
            Version of the nfcore/rnaseq pipeline
        genome_build : str
            Genome build of interest, should match the genome key in the genomes.json file

        """
        super().__init__(name=name)
        self.create_nextflow_command(revision=revision)
        self.create_nf_params(genome_build=genome_build)

    def create_nextflow_command(self, revision: str, profile: str = "docker") -> None:
        """Create a Nextflow command file within the run folder.

        Parameters
        ----------
        revision : str, optional
            Pipeline version, by default "3.18.0"
        profile : str, optional
            Nextflow profile, by default "docker"

        """
        file_path: Path = self.run_folder / "nextflow_command.txt"
        utils.processing(message=f'Creating the Nextflow command within "{file_path}"...')

        nextflow_command: str = textwrap.dedent(
            text=f"""
        nohup nextflow run nf-core/rnaseq \\
            -revision {revision} \\
            -profile {profile} \\
            -resume \\
            -params-file nf_params.json \\
        > nohup-nextflow.out \\
        2> nohup-nextflow.err
        """,
        )

        utils.string_to_textfile(text=nextflow_command, file_path=file_path)

    def create_nf_params(self, genome_build: str) -> None:
        """Create a Nextflow settings file within the run folder.

        Parameters
        ----------
        genome_build : str
            Genome build of interest, must match the key in the genomes.json file

        """
        project_settings: dict[str, str] = utils.json_to_dict(file_path=Path(".nfch/settings.json"))
        genomes: dict[str, dict[str, str]] = utils.json_to_dict(file_path=Path(".nfch/genomes.json"))
        run_settings: dict[str, str | bool] = {
            "input": "samplesheet.csv",
            "outdir": "../output",
            "email": project_settings["email"],
            "extra_salmon_quant_args": "--gcBias",
            "save_reference": "true",
        }
        if genomes[genome_build]["nfcore_rnaseq_index"]:
            # use the genome indexes if present and turn off the save_reference flag
            pass
        else:
            run_settings["fasta"] = genomes[genome_build]["fasta"]
            run_settings["gtf"] = genomes[genome_build]["gtf"]
            run_settings["save_reference"] = True
        utils.dict_to_json(dictionary=run_settings, file_path=self.nf_settings)
