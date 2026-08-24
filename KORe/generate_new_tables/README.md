# Generate New Tables

This directory contains scripts for generating new table data and reasoning pairs for the KORe (Knowledge Base Operation Recipe Reconstruction) system.

## Overview

The generation process consists of two main pipelines:
1. **Indomain pipeline** (istep*): Generate data for in-domain tasks
2. **Outdomain pipeline** (ostep*): Generate data for out-of-domain tasks with knowledge gaps

## File Structure

### Main Scripts

- `istep1_make_data.py`: Generate QA pairs for in-domain tasks
- `istep2_make_reasoning.py`: Add reasoning to in-domain QA pairs
- `istep3.py`: Additional processing for in-domain data
- `istep4_io_mix.py`: Mix in-domain and out-domain data
- `istep4_io_mix_cluster.py`: Clustered version of data mixing

- `ostep1_make_chain_gaps.py`: Create chain gaps for out-domain tasks
- `ostep2_make_data.py`: Generate QA pairs for out-domain tasks
- `ostep3_make_reasoning.py`: Add reasoning to out-domain QA pairs
- `ostep4.py`: Additional processing for out-domain data

- `fstep1_process_data.py`: Final data processing step
- `prompts.py`: Prompt templates for generation

### Directories

- `data/`: Generated data files
- `examples/`: Example files and templates

## Usage

### Environment Setup

```bash
# Activate the required conda environment
conda activate environment

# Set the working directory
cd /path/to/generate_new_tables
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
                                --train_file /path/to/train.json \
                                --model_path /path/to/model \
                                --batch_size 16 \
                                --num_examples 3
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

## Output Structure

The generated data follows this structure:
```
data/
├── qa_pairs/           # Generated QA pairs
├── qa_reasoning_pairs/ # QA pairs with reasoning
├── chains/             # Processed chain data
└── qa_pairs_gaps/     # Out-domain QA pairs
```

## Notes

1. Ensure all required dependencies are installed
2. The generation process may take several hours depending on data size and model complexity
3. Monitor the output files for any errors during processing
