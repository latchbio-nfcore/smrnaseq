
from dataclasses import dataclass
import typing
import typing_extensions

from flytekit.core.annotation import FlyteAnnotation

from latch.types.metadata import NextflowParameter
from latch.types.file import LatchFile
from latch.types.directory import LatchDir, LatchOutputDir

# Import these into your `__init__.py` file:
#
# from .parameters import generated_parameters

generated_parameters = {
    'input': NextflowParameter(
        type=LatchFile,
        default=None,
        section_title='Input/output options',
        description='Path to comma-separated file containing information about the samples in the experiment.',
    ),
    'protocol': NextflowParameter(
        type=typing.Optional[str],
        default='illumina',
        section_title=None,
        description='Protocol for constructing smRNA-seq libraries.',
    ),
    'outdir': NextflowParameter(
        type=typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})],
        default=None,
        section_title=None,
        description='The output directory where the results will be saved. You have to use absolute paths to storage on Cloud infrastructure.',
    ),
    'email': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Email address for completion summary.',
    ),
    'multiqc_title': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='MultiQC report title. Printed as page header, used for filename if not otherwise specified.',
    ),
    'with_umi': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title='UMI options',
        description='Enable UMI-based read deduplication.',
    ),
    'umitools_extract_method': NextflowParameter(
        type=typing.Optional[str],
        default='string',
        section_title=None,
        description="UMI pattern to use. Can be either 'string' (default) or 'regex'.",
    ),
    'umitools_method': NextflowParameter(
        type=typing.Optional[str],
        default='dir',
        section_title=None,
        description='UMI grouping method',
    ),
    'skip_umi_extract_before_dedup': NextflowParameter(
        type=typing.Optional[bool],
        default=True,
        section_title=None,
        description='Skip the UMI extraction from the reads before deduplication. Please note, if this parameter is set to false, the reads will be deduplicated solely on insert sequence. UMIs might be extracted after deduplication depending on the set umitools_bc_pattern nevertheless if with_umi is set to True.',
    ),
    'umitools_bc_pattern': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description="The UMI barcode pattern to use e.g. 'NNNNNN' indicates that the first 6 nucleotides of the read are from the UMI.",
    ),
    'umi_discard_read': NextflowParameter(
        type=typing.Optional[int],
        default=None,
        section_title=None,
        description='After UMI barcode extraction discard either R1 or R2 by setting this parameter to 1 or 2, respectively.',
    ),
    'save_umi_intermeds': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='If this option is specified, intermediate FastQ and BAM files produced by UMI-tools are also saved in the results directory.',
    ),
    'genome': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title='Reference genome options',
        description='Name of iGenomes reference.',
    ),
    'mirgenedb': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Boolean whether MirGeneDB should be used instead of miRBase',
    ),
    'mirtrace_species': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Species for miRTrace.',
    ),
    'mirgenedb_species': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Species of MirGeneDB.',
    ),
    'fasta': NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title=None,
        description='Path to FASTA genome file.',
    ),
    'mirna_gtf': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='GFF/GTF file with coordinates positions of precursor and miRNAs.',
    ),
    'mirgenedb_gff': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='GFF/GTF file with coordinates positions of precursor and miRNAs.',
    ),
    'mature': NextflowParameter(
        type=typing.Optional[str],
        default='https://mirbase.org/download/mature.fa',
        section_title=None,
        description='Path to FASTA file with mature miRNAs.',
    ),
    'mirgenedb_mature': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Path to FASTA file with MirGeneDB mature miRNAs.',
    ),
    'hairpin': NextflowParameter(
        type=typing.Optional[str],
        default='https://mirbase.org/download/hairpin.fa',
        section_title=None,
        description='Path to FASTA file with miRNAs precursors.',
    ),
    'mirgenedb_hairpin': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Path to FASTA file with miRNAs precursors.',
    ),
    'bowtie_index': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Path to a Bowtie 1 index directory',
    ),
    'save_reference': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Save generated reference genome files to results.',
    ),
    'save_aligned': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Save aligned reads of initial mapping in bam format.',
    ),
    'save_aligned_mirna_quant': NextflowParameter(
        type=typing.Optional[bool],
        default=True,
        section_title=None,
        description='Save aligned reads of miRNA quant subworkflow in bam format.',
    ),
    'clip_r1': NextflowParameter(
        type=typing.Optional[int],
        default=None,
        section_title='Trimming options',
        description="The number of basepairs to remove from the 5' end of read 1.",
    ),
    'three_prime_clip_r1': NextflowParameter(
        type=typing.Optional[int],
        default=None,
        section_title=None,
        description="The number of basepairs to remove from the 3' end of read 1 AFTER adapter/quality trimming has been performed.",
    ),
    'three_prime_adapter': NextflowParameter(
        type=typing.Optional[str],
        default='AGATCGGAAGAGCACACGTCTGAACTCCAGTCA',
        section_title=None,
        description='Sequencing adapter sequence to use for trimming.',
    ),
    'trim_fastq': NextflowParameter(
        type=typing.Optional[bool],
        default=True,
        section_title=None,
        description='Trim FastQ files',
    ),
    'fastp_min_length': NextflowParameter(
        type=typing.Optional[int],
        default=17,
        section_title=None,
        description='Minimum filter length for raw reads.',
    ),
    'fastp_max_length': NextflowParameter(
        type=typing.Optional[int],
        default=100,
        section_title=None,
        description='Maximum filter length for raw reads.',
    ),
    'save_trimmed_fail': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Save reads failing trimming',
    ),
    'fastp_known_mirna_adapters': NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title=None,
        description='FastA with known miRNA adapter sequences for adapter trimming',
    ),
    'min_trimmed_reads': NextflowParameter(
        type=typing.Optional[int],
        default=10,
        section_title=None,
        description='Minimum number of reads required in input file to use it',
    ),
    'save_merged': NextflowParameter(
        type=typing.Optional[bool],
        default=True,
        section_title=None,
        description='Save merged reads.',
    ),
    'phred_offset': NextflowParameter(
        type=typing.Optional[int],
        default=33,
        section_title=None,
        description='The PHRED quality offset to be used for any input fastq files. Default is 33, standard Illumina 1.8+ format.',
    ),
    'filter_contamination': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title='Contamination filter options',
        description='Enables the contamination filtering.',
    ),
    'rrna': NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title=None,
        description='Path to the rRNA fasta file to be used as contamination database.',
    ),
    'trna': NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title=None,
        description='Path to the tRNA fasta file to be used as contamination database.',
    ),
    'cdna': NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title=None,
        description='Path to the cDNA fasta file to be used as contamination database.',
    ),
    'ncrna': NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title=None,
        description='Path to the ncRNA fasta file to be used as contamination database.',
    ),
    'pirna': NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title=None,
        description='Path to the piRNA fasta file to be used as contamination database.',
    ),
    'other_contamination': NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title=None,
        description='Path to an additional fasta file to be used as contamination database.',
    ),
    'skip_fastqc': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title='Skipping pipeline steps',
        description='Skip FastQC',
    ),
    'skip_mirdeep': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Skip miRDeep',
    ),
    'skip_multiqc': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Skip MultiQC',
    ),
    'skip_fastp': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Skip FastP',
    ),
    'multiqc_methods_description': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title='Generic options',
        description='Custom MultiQC yaml file containing HTML including a methods description.',
    ),
}

