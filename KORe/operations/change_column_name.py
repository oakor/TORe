import re
from typing import List, Tuple, Dict, Any
import copy

def extract_change_column_name_params(llm_output: str) -> Tuple[str, str]:
    """
    LLMf_change_column_name
    
    Args:
        llm_output: LLM
        
    Returns:
        
    """
    # f_change_column_name
    pattern = r"f_change_column_name\((.*?)\)"
    match = re.search(pattern, llm_output, re.IGNORECASE)
    
    if not match:
        return "", ""
        
    # 
    params_str = match.group(1)
    
    # 
    params = [param.strip().strip('\'"') for param in params_str.split(',')]
    
    if len(params) != 2:
        return "", ""
        
    return params[0], params[1]

def validate_column_name(column: str, existing_columns: List[str]) -> bool:
    """
    
    
    Args:
        column: 
        existing_columns: 
        
    Returns:
        
    """
    # 
    if not column or not column.strip():
        return False
        
    # 
    if column.lower() in [col.lower() for col in existing_columns]:
        return False
        
    # 
    if re.search(r'[^\w\s-]', column):
        return False
        
    return True

def process_change_column_name(table_data: List[List[Any]], old_column: str, new_column: str) -> List[List[Any]]:
    """
    
    
    Args:
        table_data: 
        old_column: 
        new_column: 
        
    Returns:
        
    """
    if not table_data or len(table_data) < 1:
        return []
        
    # 
    existing_columns = table_data[0]
    
    # 
    if old_column not in existing_columns:
        return []
        
    # 
    if not validate_column_name(new_column, [col for col in existing_columns if col != old_column]):
        return []
    
    # 
    new_table = [row[:] for row in table_data]
    
    # 
    col_index = existing_columns.index(old_column)
    new_table[0][col_index] = new_column
    
    return new_table 