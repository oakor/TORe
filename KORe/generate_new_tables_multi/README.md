# Generate New Tables Multi

This directory contains scripts for generating new multi-table data and reasoning pairs for the KORe (Knowledge Base Operation Recipe Reconstruction) system. This version focuses on multi-table scenarios with enhanced clustering capabilities.

## Overview

The generation process consists of two main pipelines:
1. **Indomain pipeline** (istep*): Generate data for in-domain multi-table tasks
2. **Outdomain pipeline** (ostep*): Generate data for out-of-domain multi-table tasks with knowledge gaps

## File Structure

### Main Scripts

- `istep1_make_data.py`: Generate QA pairs for in-domain multi-table tasks
- `istep2_make_reasoning.py`: Add reasoning to in-domain QA pairs
- `istep3.py`: Additional processing for in-domain data
- `istep4_io_mix.py`: Mix in-domain and out-domain data
- `istep4_io_mix_cluster.py`: Clustered version of data mixing with enhanced clustering
- `istep4_io_mix_cluster_TFIDF.py`: TF-IDF based clustering for data mixing

- `ostep1_make_chain_gaps.py`: Create chain gaps for out-domain multi-table tasks
- `ostep2_make_data.py`: Generate QA pairs for out-domain multi-table tasks
- `ostep3_make_reasoning.py`: Add reasoning to out-domain QA pairs
- `ostep4.py`: Additional processing for out-domain data

- `fstep1_process_data.py`: Final data processing step
- `prompts.py`: Prompt templates for multi-table generation
- `utils.py`: Utility functions for multi-table processing

### Directories

- `data/`: Generated data files
- `output/`: Output files and results
- `examples/`: Example files and templates

## Usage

### Environment Setup

```bash
# Activate the required conda environment
conda activate environment

# Set the working directory
cd /path/to/generate_new_tables_multi
```

### Running Individual Steps

#### In-domain Pipeline

1. **Generate QA pairs**:
```bash
python istep1_make_data.py --train_file_root /path/to/train/data \
                           --processed_file_root /path/to/processed/chains \
                           --output_file_root /path/to/output/qa_pairs \
                           --model_path /path/to/model
```

2. **Add reasoning**:
```bash
python istep2_make_reasoning.py --input_file /path/to/qa_pairs.json \
                                --output_file /path/to/reasoning_pairs.json \
                                --prompt_file /path/to/prompt.json \
                                --train_file /path/to/train.json \
                                --model_path /path/to/model \
                                --batch_size 16 \
                                --num_examples 3
```

3. **Enhanced clustering** (optional):
```bash
python istep4_io_mix_cluster.py --input_file /path/to/input.json \
                                --output_file /path/to/output.json \
                                --cluster_method kmeans
```

#### Out-domain Pipeline

1. **Create chain gaps**:
```bash
python ostep1_make_chain_gaps.py
```

2. **Generate QA pairs**:
```bash
python ostep2_make_data.py --train_file_root /path/to/train/data \
                           --processed_file_root /path/to/processed/chains_gaps \
                           --output_file_root /path/to/output/qa_pairs_gaps \
                           --model_path /path/to/model
```

3. **Add reasoning**:
```bash
python ostep3_make_reasoning.py --input_file /path/to/qa_pairs_gaps.json \
                                --output_file /path/to/reasoning_pairs_gaps.json \
                                --prompt_file /path/to/prompt_gaps.json \
                                --train_file /path/to/train.json \
                                --model_path /path/to/model \
                                --batch_size 16 \
                                --num_examples 3
```

## Parameters

### Common Parameters

- `--model_path`: Path to the language model (e.g., Meta-Llama-3.1-70B-Instruct)
- `--batch_size`: Batch size for processing (default: 16)
- `--num_examples`: Number of examples to use (default: 3)

### Data Paths

- `--train_file_root`: Root directory containing training data
- `--processed_file_root`: Root directory for processed chain data
- `--output_file_root`: Root directory for output QA pairs
- `--input_file`: Input file path for specific processing steps
- `--output_file`: Output file path for specific processing steps
- `--prompt_file`: Prompt file path for reasoning generation

### Multi-table Specific Parameters

- `--cluster_method`: Clustering method for data mixing (kmeans, tfidf, etc.)
- `--num_clusters`: Number of clusters for data organization
- `--similarity_threshold`: Threshold for similarity-based clustering

## Output Structure

The generated data follows this structure:
```
data/
├── qa_pairs/                    # Generated QA pairs
├── qa_reasoning_pairs/          # QA pairs with reasoning
├── qa_pairs_gaps/              # Out-domain QA pairs
├── qa_reasoning_pairs_gaps/    # Out-domain QA pairs with reasoning
├── chains/                     # Processed chain data
└── prompt/                     # Prompt templates
```

## Multi-table Features

This version includes enhanced features for multi-table scenarios:

1. **Enhanced Clustering**: Multiple clustering methods for better data organization
2. **TF-IDF Clustering**: Text-based similarity clustering using TF-IDF
3. **Multi-table Operations**: Support for operations across multiple tables
4. **Advanced Reasoning**: Enhanced reasoning generation for complex multi-table scenarios

## Notes

1. Ensure all required dependencies are installed
2. The generation process may take several hours depending on data size and model complexity
3. Monitor the output files for any errors during processing
4. Multi-table processing requires more memory and computational resources
5. Use appropriate clustering methods based on your data characteristics
