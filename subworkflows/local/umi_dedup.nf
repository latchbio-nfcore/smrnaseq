//
// Deduplicate the UMI reads by mapping them to the complete genome.
//

include { INDEX_GENOME                        } from '../../modules/local/bowtie_genome'
include { BOWTIE_MAP_SEQ as UMI_MAP_GENOME    } from '../../modules/local/bowtie_map_mirna'
include { BAM_SORT_STATS_SAMTOOLS             } from '../../subworkflows/nf-core/bam_sort_stats_samtools'
include { UMICOLLAPSE                         } from '../../modules/nf-core/umicollapse/main'
include { SAMTOOLS_BAM2FQ                     } from '../../modules/nf-core/samtools/bam2fq/main'
include { CAT_CAT                             } from '../../modules/nf-core/cat/cat/main'
include { FASTQC as FASTQC_DEDUPLICATED        } from '../../modules/nf-core/fastqc/main'


workflow DEDUPLICATE_UMIS {
    take:
    bt_index
    reads      // channel: [ val(meta), [ reads ] ]

    main:

    ch_versions = Channel.empty()

    UMI_MAP_GENOME ( reads, bt_index.collect() )
    ch_versions = ch_versions.mix(UMI_MAP_GENOME.out.versions)

    BAM_SORT_STATS_SAMTOOLS ( UMI_MAP_GENOME.out.bam, Channel.empty() )
    ch_versions = ch_versions.mix(BAM_SORT_STATS_SAMTOOLS.out.versions)

    ch_umi_dedup = BAM_SORT_STATS_SAMTOOLS.out.bam.join(BAM_SORT_STATS_SAMTOOLS.out.bai)
    UMICOLLAPSE(ch_umi_dedup)
    ch_versions = ch_versions.mix(UMICOLLAPSE.out.versions)

    SAMTOOLS_BAM2FQ ( UMICOLLAPSE.out.bam, false )
    ch_versions = ch_versions.mix(SAMTOOLS_BAM2FQ.out.versions)

    ch_dedup_reads = SAMTOOLS_BAM2FQ.out.reads

    FASTQC_DEDUPLICATED(ch_dedup_reads)

    emit:
    reads = ch_dedup_reads
    fastqc_html = FASTQC_DEDUPLICATED.out.html
    fastqc_zip = FASTQC_DEDUPLICATED.out.zip
    indices  = bt_index
    versions = ch_versions
}
