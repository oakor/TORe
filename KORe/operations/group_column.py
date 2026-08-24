import re
from typing import List, Dict, Any
from collections import defaultdict

def extract_group_column_params(llm_output: str) -> str:
    """
    LLMf_group_column
    """
    pattern = r"f_group_column\((.*?)\)"
    match = re.search(pattern, llm_output, re.IGNORECASE)
    if not match:
        return ""
    columns = match.group(1).strip()
    # 
    columns = columns.split(',')
    columns = [col.strip('\'"') for col in columns]
    return columns

def process_group_column(table_data: List[List[Any]], group_columns: List[str]) -> List[List[Any]]:
    """
    
    
    Args:
        table_data: 
        group_column: 
        
    Returns:
        ，
    """
    # 
    try:
        header = table_data[0]
        col_index = [header.index(col.lower()) for col in group_columns]
    except ValueError:
        return table_data
    
    # 
    groups = defaultdict(int)
    
    # 
    for row in table_data[1:]:
        group_value = tuple(row[i] for i in col_index)
        groups[group_value] += 1
    
    # 
    new_table = [
        [",".join(group_columns), "count"]  # 
    ]
    
    # 
    for group_value, count in groups.items():
        new_table.append([",".join(group_value), count])
    
    return new_table 