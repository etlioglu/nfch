"""Classes representing nfcore workflows."""

import textwrap
from pathlib import Path

from nfch import utils


class Workflow:
    """A class representing generic workflows."""

    # Add the clean functionality

    def __init__(self, wf_name: str, revision: str, wf_folder: Path) -> None:
        """Instantiate the generic Workflow object and create the necessary folders.

        Parameters
        ----------
        wf_name : str | None, optional
            _description_, by default None
        wf_folder : Path | None, optional
            _description_, by default None

        """
        self.wf_name: str = wf_name
        self.revision: str = revision
        self.wf_folder: Path = wf_folder
        self.metadata_folder: Path = self.wf_folder / "metadata"
        self.run_folder: Path = self.wf_folder / "run"
        self.output_folder: Path = self.wf_folder / "output"
        self.nf_settings: Path = self.run_folder / "nf_params.json"

        project_settings: dict[str, str] = utils.json_to_dict(file_path=Path(".nfch/settings.json"))

        self.run_settings: dict[str, str | bool | int | float] = {}
        self.run_settings["input"] = "samplesheet.csv"
        self.run_settings["outdir"] = "../output"
        self.run_settings["email"] = project_settings["email"]

        # create folder for the workflow of interest
        utils.create_folder(folder_path=self.wf_folder)

        # create subfolder for metadata: sample sheet, contrast sheet, etc.
        utils.create_folder(folder_path=self.metadata_folder)

        # create subfolder for the run: Nextflow command, settings, etc.
        utils.create_folder(folder_path=self.run_folder)

        # create subfolder for the output
        utils.create_folder(folder_path=self.output_folder)

    def create_nextflow_command(self, profile: str) -> None:
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
        nohup nextflow run {self.wf_name} \\
            -revision {self.revision} \\
            -profile {profile} \\
            -resume \\
            -params-file nf_params.json \\
        > nohup_nextflow.out \\
        2> nohup_nextflow.err
        """,
        )

        utils.string_to_textfile(text=nextflow_command, file_path=file_path)


class RNASeq(Workflow):
    """A class representing nfcore/rnaseq workflows."""

    def __init__(self, revision: str, genome_build: str) -> None:
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
        self.genome_build: str = genome_build

        super().__init__(wf_name=r"nf-core/rnaseq", revision=revision, wf_folder=Path("nfcore_rnaseq"))
        super().create_nextflow_command(profile="docker")
        self.create_nf_params()

    def create_nf_params(self) -> None:
        """Create a Nextflow settings file within the run folder.

        Parameters
        ----------
        genome_build : str
            Genome build of interest, must match the key in the genomes.json file

        """
        genomes: dict[str, dict[str, str]] = utils.json_to_dict(file_path=Path(".nfch/genomes.json"))
        self.run_settings["extra_salmon_quant_args"] = "--gcBias"
        self.run_settings["fasta"] = genomes[self.genome_build]["fasta"]
        self.run_settings["gtf"] = genomes[self.genome_build]["gtf"]

        if genomes[self.genome_build]["nfcore_rnaseq_index"]:
            # use the genome indexes if present and turn off the save_reference flag
            nfcore_rnaseq_index_path: Path = Path(genomes[self.genome_build]["nfcore_rnaseq_index"])
            self.run_settings["save_reference"] = False
            self.run_settings["star_index"] = str(object=nfcore_rnaseq_index_path / "index" / "star")
            self.run_settings["salmon_index"] = str(object=nfcore_rnaseq_index_path / "index" / "salmon")
            self.run_settings["gene_bed"] = str(object=next(nfcore_rnaseq_index_path.glob(pattern="*.bed")))
        else:
            self.run_settings["save_reference"] = True
            utils.warning(
                message="Do not forget to transfer the generated genome indexes to the appropriate location with"
                "something like 'rsync -ahr --progress genome /home/eetlioglu/references/GRCh38_Ensembl/release_113/'",
            )
        utils.dict_to_json(dictionary=self.run_settings, file_path=self.nf_settings)


class DiffAbun(Workflow):
    """To be implemented."""

    def __init__(self, revision: str, genome_build: str) -> None:
        super().__init__(
            wf_name=r"nf-core/differentialabundance",
            revision=revision,
            wf_folder=Path("nfcore_differentialabundance"),
        )
        super().create_nextflow_command(profile="rnaseq,docker")
        self.create_nf_params()

    def create_nf_params(self, organism: str = "human") -> None:
        nfcore_rnaseq_params: dict[str, str | bool] = utils.json_to_dict(
            file_path=Path("nfcore_rnaseq/run/nf_params.json"),
        )

        signatures: dict[str, dict[str, str]] = utils.json_to_dict(
            file_path=Path("/home/eetlioglu/references/msigdb/signatures.json"),
        )
        expected_signatures = ["H", "C2", "C3", "C5", "C8"]
        expected_signatures = [signatures[organism][sig.lower() + ".all"] for sig in expected_signatures]
        expected_signatures_as_str = ",".join(expected_signatures)

        self.run_settings["input"] = "../../nfcore_rnaseq/run/samplesheet.csv"
        self.run_settings["contrasts"] = "../metadata/contrasts.csv"
        self.run_settings["matrix"] = (
            "../../nfcore_rnaseq/output/star_salmon/salmon.merged.gene_counts_length_scaled.tsv"
        )
        self.run_settings["gtf"] = nfcore_rnaseq_params["gtf"]
        self.run_settings["differential_min_fold_change"] = 2
        self.run_settings["differential_max_qval"] = 0.05
        self.run_settings["gsea_run"] = True
        self.run_settings["gsea_metric"] = "log2_Ratio_of_Classes"
        self.run_settings["gene_sets_files"] = expected_signatures_as_str
        self.run_settings["gsea_plot_top_x"] = 20
        self.run_settings["gprofiler2_run"] = True
        self.run_settings["gprofiler2_organism"] = "hsapiens"
        utils.dict_to_json(dictionary=self.run_settings, file_path=self.nf_settings)
