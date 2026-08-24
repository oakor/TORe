import re
from typing import List, Any, Set
import copy

def extract_select_row_params(llm_output: str) -> List[int]:
    """
    LLMf_select_row
    
    Args:
        llm_output: LLM
        
    Returns:
        （1）
    """
    # f_select_row
    pattern = r"f_select_row\((.*?)\)"
    match = re.search(pattern, llm_output, re.IGNORECASE)
    
    if not match:
        return []
        
    # 
    params_str = match.group(1)
    
    # 
    row_pattern = r"row\s+(\d+)"
    row_numbers = []
    for num in re.findall(row_pattern, params_str):
        try:
            row_num = int(num)
            if row_num > 0:  # 
                row_numbers.append(row_num)
        except ValueError:
            continue
    
    # 
    return sorted(set(row_numbers))

def validate_row_numbers(row_numbers: List[int], table_length: int) -> List[int]:
    """
    
    
    Args:
        row_numbers: 
        table_length: 
        
    Returns:
        
    """
    valid_rows = []
    for row_num in row_numbers:
        if 1 <= row_num < table_length:  # 
            valid_rows.append(row_num)
    return valid_rows

def process_select_row(table_data: List[List[Any]], selected_rows: List[int]) -> List[List[Any]]:
    """
    
    
    Args:
        table_data: 
        selected_rows: （1）
        
    Returns:
        
    """
    if not table_data or len(table_data) < 2:  # 
        return table_data
    
    # 
    valid_rows = validate_row_numbers(selected_rows, len(table_data))
    
    # ，
    if not valid_rows:
        return [table_data[0]]
    
    # ，
    new_table = [table_data[0]]  # 
    
    # 
    for row_num in valid_rows:
        new_table.append(copy.deepcopy(table_data[row_num]))
    
    return new_table 