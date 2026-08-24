import re
from typing import List, Any, Set
import copy

def extract_select_column_params(llm_output: str) -> List[str]:
    """
    LLMf_select_column
    
    Args:
        llm_output: LLM
        
    Returns:
        
    """
    # f_select_column
    pattern = r"f_select_column\((.*?)\)"
    match = re.search(pattern, llm_output, re.IGNORECASE)
    
    if not match:
        return []
        
    # 
    params_str = match.group(1)
    
    # 
    columns = []
    for col in params_str.split(','):
        col = col.strip()
        # 
        col = col.strip('\'"')
        if col:
            columns.append(col)
    
    return columns

def validate_column_names(columns: List[str], header: List[str]) -> List[str]:
    """
    
    
    Args:
        columns: 
        header: 
        
    Returns:
        
    """
    valid_columns = []
    header_lower = [h.lower() for h in header]
    
    for col in columns:
        try:
            idx = header_lower.index(col.lower())
            valid_columns.append(header[idx])  # 
        except ValueError:
            continue
    
    return valid_columns

def process_select_column(table_data: List[List[Any]], selected_columns: List[str]) -> List[List[Any]]:
    """
    
    
    Args:
        table_data: 
        selected_columns: 
        
    Returns:
        
    """
    if not table_data or len(table_data) < 1:
        return [[]]
        
    # 
    header = table_data[0]
    
    # 
    valid_columns = validate_column_names(selected_columns, header)
    
    # ，
    if not valid_columns:
        return [[]]
    
    # 
    col_indices = [header.index(col) for col in valid_columns]
    
    # ，
    new_table = []
    for row in table_data:
        new_row = [row[i] for i in col_indices]
        new_table.append(new_row)
    
    return new_table 