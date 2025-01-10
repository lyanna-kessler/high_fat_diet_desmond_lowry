# Lyanna Kessler
# 9/6/23

# make an environment:
"""
Go to install QIIME page and it teaches you how to make a conda environment

"""

# Run this before starting any code
# conda activate /opt/anaconda3/envs/qiime2-2023.7

# Then navigate to your code folder
# cd high_fat_microbiome/

'''

mkdir raw_sequences
mv Undetermined* raw_sequences
cd raw_sequences

mv Undetermined_S0_L001_I1_001.fastq.gz barcodes.fastq.gz
mv Undetermined_S0_L001_R1_001.fastq.gz forward.fastq.gz
mv Undetermined_S0_L001_R2_001.fastq.gz reverse.fastq.gz
cd ..

qiime tools import \
--type EMPPairedEndSequences \
--input-path raw_sequences \
--output-path paired-end-sequences.qza

qiime demux emp-paired \
--m-barcodes-file high_fat_metadata.tsv \
--m-barcodes-column Barcode \
--i-seqs paired-end-sequences.qza \
--p-rev-comp-barcodes \
--p-rev-comp-mapping-barcodes \
--output-dir demux 

qiime demux summarize \
--i-data demux/per_sample_sequences.qza \
--o-visualization demux/demux.qzv
'''

# go to qiime viewer website and view demux.qzv
# least reads: 11841, sample 10-1-4
# most reads: 123096, sample 45-3-1
# median quality score: 33

'''
# this one takes awhile
# trim barcodes up to 19-20
# trim 150 instead of 151 since read 151 has low quality
qiime dada2 denoise-paired \
--i-demultiplexed-seqs demux/per_sample_sequences.qza \
--p-trunc-len-f 150 \
--p-trunc-len-r 150 \
--p-trim-left-f 20 \
--p-trim-left-r 20 \
--output-dir dada2-results/

qiime feature-table summarize \
--i-table dada2-results/table.qza \
--o-visualization dada2-results/table.qzv \
--m-sample-metadata-file high_fat_metadata.tsv

'''

# shortest read: 8596, sample 10-1-4
# second shortest: 14966, sample 10-1-3
# longest read: 94134, sample 45-3-1

'''
# longest one
qiime fragment-insertion sepp \
--i-representative-sequences dada2-results/representative_sequences.qza \
--i-reference-database sepp-refs-silva-128.qza \
--o-tree insertion-tree.qza \
--o-placements insertion-placements.qza

qiime fragment-insertion filter-features \
--i-table dada2-results/table.qza \
--i-tree insertion-tree.qza \
--o-filtered-table filtered-table.qza \
--o-removed-table removed-table.qza

qiime feature-classifier classify-sklearn \
--i-reads dada2-results/representative_sequences.qza \
--i-classifier silva-138-99-515-806-nb-classifier.qza \
--output-dir silva-classified

qiime metadata tabulate \
--m-input-file silva-classified/classification.qza \
--o-visualization silva-classified/classification.qzv

mv silva-classified/classification.qza taxonomy-silva.qza
mv silva-classified/classification.qzv taxonomy-silva.qzv

qiime taxa filter-table \
  --i-table filtered-table.qza \
  --i-taxonomy taxonomy-silva.qza \
  --p-exclude mitochondria,chloroplast \
  --o-filtered-table noMito_noChloro-filtered-table.qza
  
qiime taxa barplot \
--i-table noMito_noChloro-filtered-table.qza \
--i-taxonomy taxonomy-silva.qza \
--m-metadata-file high_fat_metadata.tsv \
--o-visualization taxa-barplot.qzv

mv noMito_noChloro-filtered-table.qza  hf_table.qza

qiime diversity core-metrics-phylogenetic \
  --i-phylogeny insertion-tree.qza \
  --i-table hf_table.qza \
  --p-sampling-depth 8595 \
  --m-metadata-file high_fat_metadata.tsv \
  --output-dir core-diversity-results

  
qiime diversity alpha-group-significance \
--i-alpha-diversity core-diversity-results/faith_pd_vector.qza \
--m-metadata-file high_fat_metadata.tsv \
--o-visualization core-diversity-results/faith-pd-group-significance.qzv

qiime diversity alpha-correlation \
--i-alpha-diversity core-diversity-results/faith_pd_vector.qza \
--m-metadata-file high_fat_metadata.tsv \
--o-visualization core-diversity-results/faith-pd-correlation.qzv

'''

# TAKE OUT CONTROLS

"""
qiime feature-table filter-samples \
  --i-table hf_table.qza \
  --m-metadata-file high_fat_metadata.tsv \
  --p-where "[Treatment] IN ('CD','WD')" \
  --o-filtered-table hf_noctrl_table.qza

qiime diversity core-metrics-phylogenetic \
  --i-phylogeny insertion-tree.qza \
  --i-table hf_noctrl_table.qza \
  --p-sampling-depth 8595 \
  --m-metadata-file high_fat_metadata.tsv \
  --output-dir core-diversity-results2

"""

# Add weight metric with new metadata from Luke
# Metadata has no controls
# No animals that died midway either

"""
qiime feature-table filter-samples \
  --i-table hf_table.qza \
  --m-metadata-file hf_meta_weights.tsv \
  --o-filtered-table hf_weights_table.qza

qiime diversity core-metrics-phylogenetic \
  --i-phylogeny insertion-tree.qza \
  --i-table hf_weights_table.qza \
  --p-sampling-depth 8595 \
  --m-metadata-file hf_meta_weights.tsv \
  --output-dir cd_new_results

qiime diversity alpha-group-significance \
--i-alpha-diversity cd_new_results/faith_pd_vector.qza \
--m-metadata-file hf_meta_weights.tsv \
--o-visualization cd_new_results/faith-pd-group-significance.qzv

qiime diversity alpha-group-significance \
--i-alpha-diversity cd_new_results/shannon_vector.qza \
--m-metadata-file hf_meta_weights.tsv \
--o-visualization cd_new_results/shannon_group_signif.qzv

qiime diversity alpha-group-significance \
--i-alpha-diversity cd_new_results/evenness_vector.qza \
--m-metadata-file hf_meta_weights.tsv \
--o-visualization cd_new_results/evenness_group_signif.qzv

"""


# get rep seqs for BLAST

"""
qiime feature-table tabulate-seqs \
--i-data dada2-results/representative_sequences.qza \
--o-visualization dada2-results/rep_seqs.qzv

"""