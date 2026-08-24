# Knowledge Base Operation Recipe Reconstruction (KORe)

This is a table question-answering system based on vLLM that processes table questions step by step through KBOR.

## Features

1. Uses vLLM for efficient inference
2. Supports multiple table operations:
   - add_column:add new columns
   - sort_column:sort by column
   - select_column:select specific columns
   - select_row:select specific rows
   - group_column:group by column
   - add_knowledge_column:add column of lacked knowledge
   - add_inferred_knowledge:add column inferred from other knowledge
   - stitch_tables:stitch tables
   - select_table:select one table
   - change_column_name:change specific column name
3. Executes only one operation at a time and generates a new table
4. Supports chained operations, with a maximum of 5 operations

## Installation

```bash
pip install -r requirements.txt
```

## Usage

1. Prepare input file (JSON format):
```json
[
    {
        "statement": "Question description",
        "table_caption": "Table title (optional)",
        "table_info": {
            "table_text": [
                ["Column1", "Column2", "Column3"],
                ["Value1", "Value2", "Value3"],
                ["Value4", "Value5", "Value6"]
            ]
        }
    }
]
```

2. Run the program:
```bash
python main.py \
    --model_path /path/to/model \
    --input_file input.json \
    --output_file output.json \
    --max_operations 5
```

## Output Format

```json
[
    {
        "statement": "Question description",
        "table_caption": "Table title",
        "chain": ["Operation1", "Operation2", ...],
        "answer": "Final answer"
    }
]
```

## Notes

1. Ensure the input file format is correct
2. Tables must be in valid markdown format
3. Each operation generates a new table
4. When the model selects the END operation, it generates the final answer 




## Data construction
Please refer to README.md in the 'generate_new_tables' or the 'generate_new_tables_multi' directory.