"""
Store prompts for different stages of question generation
"""
from examples.task_0 import task_0_EXAMPLES_single, task_0_EXAMPLES_multi
from examples.task_1 import task_1_EXAMPLES_single, task_1_EXAMPLES_multi
from examples.task_2 import task_2_EXAMPLES_single, task_2_EXAMPLES_multi
from examples.task_3 import task_3_EXAMPLES_single, task_3_EXAMPLES_multi
from examples.task_4 import task_4_EXAMPLES_single, task_4_EXAMPLES_multi
from examples.task_5 import task_5_EXAMPLES_single, task_5_EXAMPLES_multi
from examples.task_6 import task_6_EXAMPLES_single, task_6_EXAMPLES_multi
from examples.task_7 import task_7_EXAMPLES_single, task_7_EXAMPLES_multi
from examples.task_8 import task_8_EXAMPLES_single, task_8_EXAMPLES_multi
import random

EXAMPLES_single = [task_0_EXAMPLES_single, task_1_EXAMPLES_single, task_2_EXAMPLES_single, task_3_EXAMPLES_single, task_4_EXAMPLES_single, task_5_EXAMPLES_single, task_6_EXAMPLES_single, task_7_EXAMPLES_single, task_8_EXAMPLES_single]
EXAMPLES_multi = [task_0_EXAMPLES_multi, task_1_EXAMPLES_multi, task_2_EXAMPLES_multi, task_3_EXAMPLES_multi, task_4_EXAMPLES_multi, task_5_EXAMPLES_multi, task_6_EXAMPLES_multi, task_7_EXAMPLES_multi, task_8_EXAMPLES_multi]

# Stage 1: Chain Parameter Generation
CHAIN_PARAM_PROMPT = """You are a table operation parameter generation assistant. Your task is to fill in the parameters for each operation in the chain based on the given table.

For each operation in the chain, you need to:
1. Analyze the table structure and content
2. Determine appropriate parameters for each operation
3. Ensure the parameters are valid and meaningful
4. New intermediate table should be inferred from the last intermediate table

Available Operations and their parameter requirements:
- f_add_knowledge_column(column_name): Add a new column that requires external knowledge
- f_add_inferred_column(column_name): Add a new column that can be calculated or inferred from existing columns
- f_sort_column(column_name): Sort the table by a specific column
- f_select_column(column1, column2, ...): Select specific columns from the table
- f_select_row(row1, row2, ...): Select specific rows from the table
- f_group_column(column_name): Group the table by only one specific column, the output table should only have the specified column and the count column
- f_change_column_name(old_name, new_name): Rename a column
- f_stitch_tables(table1.column1, table2.column2, join_method): Stitch two tables together by a specific column, choose join_method in [inner, left, right]
- f_select_table(table_name): Select a specific table from the database

Please output in the following format:
Operation 1: [operation with filled parameters]
Explanation: [explain why these parameters were chosen]
Intermediate Table: [show the table after this operation]

Operation 2: [operation with filled parameters]
Explanation: [explain why these parameters were chosen]
Intermediate Table: [show the table after this operation]

# Example 1:
## Table Information:
{table_info_example_1}
## Operation Chain:
{chain_example_1}
## Filled Chain:
{filled_chain_example_1}

# Example 2:
## Table Information:
{table_info_example_2}
## Operation Chain:
{chain_example_2}
## Filled Chain:
{filled_chain_example_2}

# Example 3:
## Table Information:
{table_info_example_3}
## Operation Chain:
{chain_example_3}
## Filled Chain:
{filled_chain_example_3}

# Your Turn:
## Table Information:
{table_info}
## Operation Chain:
{chain}
## Filled Chain:
"""

CHAIN_PARAM_PROMPT_AUX = """
Operation {idx}: [operation with filled parameters]
Explanation: [explain why these parameters were chosen]
Intermediate Table: [show the table after this operation]

"""

# # Stage 2: Table Processing
# TABLE_PROCESSING_PROMPT = """You are a table processing assistant. Your task is to process the table according to the given operation chain with parameters.

# Table Information:
# {table_info}

# Operation Chain with Parameters:
# {chain_with_params}

# For each operation:
# 1. Verify the parameters are valid
# 2. Apply the operation to the table
# 3. Show the intermediate result

# Please process the table step by step and show the result after each operation.
# """

# Stage 3: Question and Answer Generation
QA_GENERATION_PROMPT = """You are a table question generation assistant. Your task is to generate a natural question and its corresponding answer based on the table processing steps.

Please generate a question and answer that:
1. Requires all the operations in the chain to solve
2. Can be answered using the final table
3. Is natural and clear
4. Has a precise answer

Please output in the following format:
Question: [generated question]
Answer: [generated answer]
Explanation: [explain how the operations help answer this question]

# Example 1:
## Original Table:
{original_table_example_1}
## Operation Chain with Parameters:
{chain_with_params_example_1}
## Final Table:
{final_table_example_1}
## Question:
{question_example_1}
## Answer:
{answer_example_1}
## Explanation:
{explanation_example_1}

# Example 2:
## Original Table:
{original_table_example_2}
## Operation Chain with Parameters:
{chain_with_params_example_2}
## Final Table:
{final_table_example_2}
## Question:
{question_example_2}
## Answer:
{answer_example_2}
## Explanation:
{explanation_example_2}

# Example 3:
## Original Table:
{original_table_example_3}
## Operation Chain with Parameters:
{chain_with_params_example_3}
## Final Table:
{final_table_example_3}
## Question:
{question_example_3}
## Answer:
{answer_example_3}
## Explanation:
{explanation_example_3}

# Your Turn:
## Original Table:
{original_table}
## Operation Chain with Parameters:
{chain_with_params}
## Final Table:
{final_table}
## Question:
"""


def generate_chain_param_prompt(table_info: str, chain: list, task_id: int, random_seed: int, is_multi_table: bool = False) -> str:
    """Generate prompt for chain parameter generation"""
    random.seed(random_seed)
    if is_multi_table:
        task_example = EXAMPLES_multi[task_id]
    else:
        task_example = EXAMPLES_single[task_id]
    keys = list(task_example.keys())
    random.shuffle(keys)
    EXAMPLE_1 = task_example[keys[0]]
    EXAMPLE_2 = task_example[keys[1]]
    import json
    with open("help.json", "w") as f:
        json.dump(EXAMPLE_2 , f, indent=4)
    EXAMPLE_3 = task_example[keys[2]]
    
    return CHAIN_PARAM_PROMPT.format(
        table_info_example_1=EXAMPLE_1["table_info"],
        chain_example_1=EXAMPLE_1["chain"],
        filled_chain_example_1="".join([CHAIN_PARAM_PROMPT_AUX.format(idx=i, operation=operation).replace("[operation with filled parameters]", EXAMPLE_1["filled_chain"][i]).replace("[explain why these parameters were chosen]", EXAMPLE_1["explanations"][i]).replace("[show the table after this operation]", EXAMPLE_1["intermediate_tables"][i]) for i, operation in enumerate(EXAMPLE_1["filled_chain"][:-1])]),
        table_info_example_2=EXAMPLE_2["table_info"],
        chain_example_2=EXAMPLE_2["chain"],
        filled_chain_example_2="".join([CHAIN_PARAM_PROMPT_AUX.format(idx=i, operation=operation).replace("[operation with filled parameters]", EXAMPLE_2["filled_chain"][i]).replace("[explain why these parameters were chosen]", EXAMPLE_2["explanations"][i]).replace("[show the table after this operation]", EXAMPLE_2["intermediate_tables"][i]) for i, operation in enumerate(EXAMPLE_2["filled_chain"][:-1])]),
        table_info_example_3=EXAMPLE_3["table_info"],
        chain_example_3=EXAMPLE_3["chain"],
        filled_chain_example_3="".join([CHAIN_PARAM_PROMPT_AUX.format(idx=i, operation=operation).replace("[operation with filled parameters]", EXAMPLE_3["filled_chain"][i]).replace("[explain why these parameters were chosen]", EXAMPLE_3["explanations"][i]).replace("[show the table after this operation]", EXAMPLE_3["intermediate_tables"][i]) for i, operation in enumerate(EXAMPLE_3["filled_chain"][:-1])]),
        table_info=table_info,
        chain=chain
    )

# def generate_table_processing_prompt(table_info: str, chain_with_params: list) -> str:
#     """Generate prompt for table processing"""
#     return TABLE_PROCESSING_PROMPT.format(
#         table_info=table_info,
#         chain_with_params=chain_with_params
#     )

def generate_qa_prompt(original_table: str, chain_with_params: list, 
                      final_table: str, task_id: int, random_seed: int, is_multi_table: bool = False) -> str:
    """Generate prompt for question and answer generation"""
    random.seed(random_seed)
    if is_multi_table:
        task_example = EXAMPLES_multi[task_id]
    else:
        task_example = EXAMPLES_single[task_id]
    keys = list(task_example.keys())
    random.shuffle(keys)
    EXAMPLE_1 = task_example[keys[0]]
    EXAMPLE_2 = task_example[keys[1]]
    EXAMPLE_3 = task_example[keys[2]]
    
    return QA_GENERATION_PROMPT.format(
        original_table_example_1=EXAMPLE_1["table_info"],
        chain_with_params_example_1=EXAMPLE_1["filled_chain"],
        final_table_example_1=EXAMPLE_1["intermediate_tables"][-1],
        question_example_1=EXAMPLE_1["question"],
        answer_example_1=EXAMPLE_1["answer"],
        explanation_example_1=EXAMPLE_1["explanation"],
        original_table_example_2=EXAMPLE_2["table_info"],
        chain_with_params_example_2=EXAMPLE_2["filled_chain"],
        final_table_example_2=EXAMPLE_2["intermediate_tables"][-1],
        question_example_2=EXAMPLE_2["question"],
        answer_example_2=EXAMPLE_2["answer"],
        explanation_example_2=EXAMPLE_2["explanation"],
        original_table_example_3=EXAMPLE_3["table_info"],
        chain_with_params_example_3=EXAMPLE_3["filled_chain"],
        final_table_example_3=EXAMPLE_3["intermediate_tables"][-1],
        question_example_3=EXAMPLE_3["question"],
        answer_example_3=EXAMPLE_3["answer"],
        explanation_example_3=EXAMPLE_3["explanation"],
        original_table=original_table,
        chain_with_params=chain_with_params,
        final_table=final_table
    )


f_add_inferred_column_demos = """We use f_add_inferred_column() to add one column to the table. This function is used when we need to add a column that can be calculated or inferred from existing columns. You need to add the values of the column.

## Response format
Return the values in this format:
[value1, value2, ...]

## Example 1
/*
col : year | team | games | wins | losses | points
row 1 : 2020 | Lakers | 82 | 52 | 30 | 104
row 2 : 2021 | Lakers | 82 | 42 | 40 | 84
row 3 : 2022 | Lakers | 82 | 33 | 49 | 66
row 4 : 2023 | Lakers | 82 | 32 | 50 | 64
*/
Function: f_add_inferred_column(win_percentage)
Explanation: Adding win_percentage based on the number of wins and total number of games. 
Values: [63.41, 51.22, 40.24, 39.02]
New Table:
/*
col : year | team | games | wins | losses | points | win_percentage
row 1 : 2020 | Lakers | 82 | 52 | 30 | 104 | 63.41
row 2 : 2021 | Lakers | 82 | 42 | 40 | 84 | 51.22
row 3 : 2022 | Lakers | 82 | 33 | 49 | 66 | 40.24
row 4 | 2023 | Lakers | 82  | 32 | 50 | 64 | 39.02
*/

## Example 2
/*
col : year | team | games | combined tackles | tackles | assisted tackles
row 1 : 2004 | hou | 16 | 63 | 51 | 12
row 2 : 2005 | hou | 12 | 35 | 24 | 11
row 3 : 2006 | hou | 15 | 26 | 19 | 7
*/
Function: f_add_inferred_column(avg_tackles)
Explanation: Adding avg_tackles based on the number of tackles and total number of games.
Values: [3.19, 2.00, 1.27]
New Table:
/*
col : year | team | games | combined tackles | tackles | assisted tackles | avg_tackles
row 1 : 2004 | hou | 16 | 63 | 51 | 12 | 3.19
row 2 : 2005 | hou | 12 | 35 | 24 | 11 | 2.00
row 3 : 2006 | hou | 15 | 26 | 19 | 7 | 1.27
*/

## Your Turn
[Insert Table Here]
Function: [Insert Function Here]
Explanation: [Insert Explanation Here]
Values: 
"""

f_add_knowledge_column_demos = """We use f_add_knowledge_column() to add one column to the table. This function is used when we need to add a column that requires external knowledge. You need to compelete the values of the column.

## Response format
Return the values in this format:
[value1, value2, ...]

## Example 1
/*
col : year | team | games | wins | losses | points
row 1 : 2020 | Lakers | 82 | 52 | 30 | 104
row 2 : 2021 | Lakers | 82 | 42 | 40 | 84
row 3 : 2022 | Lakers | 82 | 33 | 49 | 66
row 4 : 2023 | Lakers | 82 | 32 | 50 | 64
*/
Function: f_add_knowledge_column(region)
Explanation: Adding region information to identify Asian countries.
Values: [Asia, Asia, Asia, Asia]
New Table:
/*
col : year | team | games | wins | losses | points | region
row 1 : 2020 | Lakers | 82 | 52 | 30 | 104 | Asia
row 2 : 2021 | Lakers | 82 | 42 | 40 | 84 | Asia
row 3 : 2022 | Lakers | 82 | 33 | 49 | 66 | Asia
row 4 : 2023 | Lakers | 82 | 32 | 50 | 64 | Asia
*/ 

## Example 2
/*
col : date | temperature | humidity | wind_speed
row 1 : 2020-01-01 | 25 | 50 | 10
row 2 : 2020-01-02 | 20 | 60 | 15
row 3 : 2020-01-03 | 18 | 70 | 20
row 4 : 2020-01-04 | 22 | 45 | 12
*/
Function: f_add_knowledge_column(weather_type)
Explanation: Adding weather_type information to identify sunny, cloudy, rainy weather.
Values: [sunny, cloudy, rainy, sunny]
New Table:
/*
col : date | temperature | humidity | wind_speed | weather_type
row 1 : 2020-01-01 | 25 | 50 | 10 | sunny
row 2 : 2020-01-02 | 20 | 60 | 15 | cloudy
row 3 : 2020-01-03 | 18 | 70 | 20 | rainy
row 4 : 2020-01-04 | 22 | 45 | 12 | sunny
*/

## Your Turn
[Insert Table Here]
Function: [Insert Function Here]
Explanation: [Insert Explanation Here]
Values: 
"""
