from dataclasses import dataclass
from enum import Enum
import os
import subprocess
import requests
import shutil
from pathlib import Path
import typing
import typing_extensions

from latch.resources.workflow import workflow
from latch.resources.tasks import nextflow_runtime_task, custom_task
from latch.types.file import LatchFile
from latch.types.directory import LatchDir, LatchOutputDir
from latch.ldata.path import LPath
from latch_cli.nextflow.workflow import get_flag
from latch_cli.nextflow.utils import _get_execution_name
from latch_cli.utils import urljoins
from latch.types import metadata
from flytekit.core.annotation import FlyteAnnotation

from latch_cli.services.register.utils import import_module_by_path

meta = Path("latch_metadata") / "__init__.py"
import_module_by_path(meta)
import latch_metadata

@custom_task(cpu=0.25, memory=0.5, storage_gib=1)
def initialize() -> str:
    token = os.environ.get("FLYTE_INTERNAL_EXECUTION_ID")
    if token is None:
        raise RuntimeError("failed to get execution token")

    headers = {"Authorization": f"Latch-Execution-Token {token}"}

    print("Provisioning shared storage volume... ", end="")
    resp = requests.post(
        "http://nf-dispatcher-service.flyte.svc.cluster.local/provision-storage",
        headers=headers,
        json={
            "storage_gib": 100,
        }
    )
    resp.raise_for_status()
    print("Done.")

    return resp.json()["name"]






@nextflow_runtime_task(cpu=4, memory=8, storage_gib=100)
def nextflow_runtime(pvc_name: str, input: LatchFile, outdir: typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})], email: typing.Optional[str], multiqc_title: typing.Optional[str], with_umi: typing.Optional[bool], umitools_bc_pattern: typing.Optional[str], umi_discard_read: typing.Optional[int], save_umi_intermeds: typing.Optional[bool], genome: typing.Optional[str], mirgenedb: typing.Optional[bool], mirtrace_species: typing.Optional[str], mirgenedb_species: typing.Optional[str], fasta: typing.Optional[LatchFile], mirna_gtf: typing.Optional[str], mirgenedb_gff: typing.Optional[str], mirgenedb_mature: typing.Optional[str], mirgenedb_hairpin: typing.Optional[str], bowtie_index: typing.Optional[str], save_reference: typing.Optional[bool], save_aligned: typing.Optional[bool], clip_r1: typing.Optional[int], three_prime_clip_r1: typing.Optional[int], save_trimmed_fail: typing.Optional[bool], fastp_known_mirna_adapters: typing.Optional[LatchFile], filter_contamination: typing.Optional[bool], rrna: typing.Optional[LatchFile], trna: typing.Optional[LatchFile], cdna: typing.Optional[LatchFile], ncrna: typing.Optional[LatchFile], pirna: typing.Optional[LatchFile], other_contamination: typing.Optional[LatchFile], skip_fastqc: typing.Optional[bool], skip_mirdeep: typing.Optional[bool], skip_multiqc: typing.Optional[bool], skip_fastp: typing.Optional[bool], multiqc_methods_description: typing.Optional[str], protocol: typing.Optional[str], umitools_extract_method: typing.Optional[str], umitools_method: typing.Optional[str], skip_umi_extract_before_dedup: typing.Optional[bool], mature: typing.Optional[str], hairpin: typing.Optional[str], save_aligned_mirna_quant: typing.Optional[bool], three_prime_adapter: typing.Optional[str], trim_fastq: typing.Optional[bool], fastp_min_length: typing.Optional[int], fastp_max_length: typing.Optional[int], min_trimmed_reads: typing.Optional[int], save_merged: typing.Optional[bool], phred_offset: typing.Optional[int]) -> None:
    try:
        shared_dir = Path("/nf-workdir")



        ignore_list = [
            "latch",
            ".latch",
            "nextflow",
            ".nextflow",
            "work",
            "results",
            "miniconda",
            "anaconda3",
            "mambaforge",
        ]

        shutil.copytree(
            Path("/root"),
            shared_dir,
            ignore=lambda src, names: ignore_list,
            ignore_dangling_symlinks=True,
            dirs_exist_ok=True,
        )

        cmd = [
            "/root/nextflow",
            "run",
            str(shared_dir / "main.nf"),
            "-work-dir",
            str(shared_dir),
            "-profile",
            "docker",
            "-c",
            "latch.config",
                *get_flag('input', input),
                *get_flag('protocol', protocol),
                *get_flag('outdir', outdir),
                *get_flag('email', email),
                *get_flag('multiqc_title', multiqc_title),
                *get_flag('with_umi', with_umi),
                *get_flag('umitools_extract_method', umitools_extract_method),
                *get_flag('umitools_method', umitools_method),
                *get_flag('skip_umi_extract_before_dedup', skip_umi_extract_before_dedup),
                *get_flag('umitools_bc_pattern', umitools_bc_pattern),
                *get_flag('umi_discard_read', umi_discard_read),
                *get_flag('save_umi_intermeds', save_umi_intermeds),
                *get_flag('genome', genome),
                *get_flag('mirgenedb', mirgenedb),
                *get_flag('mirtrace_species', mirtrace_species),
                *get_flag('mirgenedb_species', mirgenedb_species),
                *get_flag('fasta', fasta),
                *get_flag('mirna_gtf', mirna_gtf),
                *get_flag('mirgenedb_gff', mirgenedb_gff),
                *get_flag('mature', mature),
                *get_flag('mirgenedb_mature', mirgenedb_mature),
                *get_flag('hairpin', hairpin),
                *get_flag('mirgenedb_hairpin', mirgenedb_hairpin),
                *get_flag('bowtie_index', bowtie_index),
                *get_flag('save_reference', save_reference),
                *get_flag('save_aligned', save_aligned),
                *get_flag('save_aligned_mirna_quant', save_aligned_mirna_quant),
                *get_flag('clip_r1', clip_r1),
                *get_flag('three_prime_clip_r1', three_prime_clip_r1),
                *get_flag('three_prime_adapter', three_prime_adapter),
                *get_flag('trim_fastq', trim_fastq),
                *get_flag('fastp_min_length', fastp_min_length),
                *get_flag('fastp_max_length', fastp_max_length),
                *get_flag('save_trimmed_fail', save_trimmed_fail),
                *get_flag('fastp_known_mirna_adapters', fastp_known_mirna_adapters),
                *get_flag('min_trimmed_reads', min_trimmed_reads),
                *get_flag('save_merged', save_merged),
                *get_flag('phred_offset', phred_offset),
                *get_flag('filter_contamination', filter_contamination),
                *get_flag('rrna', rrna),
                *get_flag('trna', trna),
                *get_flag('cdna', cdna),
                *get_flag('ncrna', ncrna),
                *get_flag('pirna', pirna),
                *get_flag('other_contamination', other_contamination),
                *get_flag('skip_fastqc', skip_fastqc),
                *get_flag('skip_mirdeep', skip_mirdeep),
                *get_flag('skip_multiqc', skip_multiqc),
                *get_flag('skip_fastp', skip_fastp),
                *get_flag('multiqc_methods_description', multiqc_methods_description)
        ]

        print("Launching Nextflow Runtime")
        print(' '.join(cmd))
        print(flush=True)

        env = {
            **os.environ,
            "NXF_HOME": "/root/.nextflow",
            "NXF_OPTS": "-Xms2048M -Xmx8G -XX:ActiveProcessorCount=4",
            "K8S_STORAGE_CLAIM_NAME": pvc_name,
            "NXF_DISABLE_CHECK_LATEST": "true",
        }
        subprocess.run(
            cmd,
            env=env,
            check=True,
            cwd=str(shared_dir),
        )
    finally:
        print()

        nextflow_log = shared_dir / ".nextflow.log"
        if nextflow_log.exists():
            name = _get_execution_name()
            if name is None:
                print("Skipping logs upload, failed to get execution name")
            else:
                remote = LPath(urljoins("latch:///your_log_dir/nf_nf_core_smrnaseq", name, "nextflow.log"))
                print(f"Uploading .nextflow.log to {remote.path}")
                remote.upload_from(nextflow_log)



@workflow(metadata._nextflow_metadata)
def nf_nf_core_smrnaseq(input: LatchFile, outdir: typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})], email: typing.Optional[str], multiqc_title: typing.Optional[str], with_umi: typing.Optional[bool], umitools_bc_pattern: typing.Optional[str], umi_discard_read: typing.Optional[int], save_umi_intermeds: typing.Optional[bool], genome: typing.Optional[str], mirgenedb: typing.Optional[bool], mirtrace_species: typing.Optional[str], mirgenedb_species: typing.Optional[str], fasta: typing.Optional[LatchFile], mirna_gtf: typing.Optional[str], mirgenedb_gff: typing.Optional[str], mirgenedb_mature: typing.Optional[str], mirgenedb_hairpin: typing.Optional[str], bowtie_index: typing.Optional[str], save_reference: typing.Optional[bool], save_aligned: typing.Optional[bool], clip_r1: typing.Optional[int], three_prime_clip_r1: typing.Optional[int], save_trimmed_fail: typing.Optional[bool], fastp_known_mirna_adapters: typing.Optional[LatchFile], filter_contamination: typing.Optional[bool], rrna: typing.Optional[LatchFile], trna: typing.Optional[LatchFile], cdna: typing.Optional[LatchFile], ncrna: typing.Optional[LatchFile], pirna: typing.Optional[LatchFile], other_contamination: typing.Optional[LatchFile], skip_fastqc: typing.Optional[bool], skip_mirdeep: typing.Optional[bool], skip_multiqc: typing.Optional[bool], skip_fastp: typing.Optional[bool], multiqc_methods_description: typing.Optional[str], protocol: typing.Optional[str] = 'illumina', umitools_extract_method: typing.Optional[str] = 'string', umitools_method: typing.Optional[str] = 'dir', skip_umi_extract_before_dedup: typing.Optional[bool] = True, mature: typing.Optional[str] = 'https://mirbase.org/download/mature.fa', hairpin: typing.Optional[str] = 'https://mirbase.org/download/hairpin.fa', save_aligned_mirna_quant: typing.Optional[bool] = True, three_prime_adapter: typing.Optional[str] = 'AGATCGGAAGAGCACACGTCTGAACTCCAGTCA', trim_fastq: typing.Optional[bool] = True, fastp_min_length: typing.Optional[int] = 17, fastp_max_length: typing.Optional[int] = 100, min_trimmed_reads: typing.Optional[int] = 10, save_merged: typing.Optional[bool] = True, phred_offset: typing.Optional[int] = 33) -> None:
    """
    nf-core/smrnaseq

    Sample Description
    """

    pvc_name: str = initialize()
    nextflow_runtime(pvc_name=pvc_name, input=input, protocol=protocol, outdir=outdir, email=email, multiqc_title=multiqc_title, with_umi=with_umi, umitools_extract_method=umitools_extract_method, umitools_method=umitools_method, skip_umi_extract_before_dedup=skip_umi_extract_before_dedup, umitools_bc_pattern=umitools_bc_pattern, umi_discard_read=umi_discard_read, save_umi_intermeds=save_umi_intermeds, genome=genome, mirgenedb=mirgenedb, mirtrace_species=mirtrace_species, mirgenedb_species=mirgenedb_species, fasta=fasta, mirna_gtf=mirna_gtf, mirgenedb_gff=mirgenedb_gff, mature=mature, mirgenedb_mature=mirgenedb_mature, hairpin=hairpin, mirgenedb_hairpin=mirgenedb_hairpin, bowtie_index=bowtie_index, save_reference=save_reference, save_aligned=save_aligned, save_aligned_mirna_quant=save_aligned_mirna_quant, clip_r1=clip_r1, three_prime_clip_r1=three_prime_clip_r1, three_prime_adapter=three_prime_adapter, trim_fastq=trim_fastq, fastp_min_length=fastp_min_length, fastp_max_length=fastp_max_length, save_trimmed_fail=save_trimmed_fail, fastp_known_mirna_adapters=fastp_known_mirna_adapters, min_trimmed_reads=min_trimmed_reads, save_merged=save_merged, phred_offset=phred_offset, filter_contamination=filter_contamination, rrna=rrna, trna=trna, cdna=cdna, ncrna=ncrna, pirna=pirna, other_contamination=other_contamination, skip_fastqc=skip_fastqc, skip_mirdeep=skip_mirdeep, skip_multiqc=skip_multiqc, skip_fastp=skip_fastp, multiqc_methods_description=multiqc_methods_description)

