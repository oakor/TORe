import re
from typing import List, Tuple, Dict, Any
import copy

def extract_add_column_params(llm_output: str) -> Tuple[List[str], List[List[Any]]]:
    """
    LLMf_add_column
    
    Args:
        llm_output: LLM
        
    Returns:
        
    """
    # f_add_column
    pattern = r"f_add_column\((.*?)\)"
    match = re.search(pattern, llm_output, re.IGNORECASE)
    
    if not match:
        return [], []
        
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
    
    # 
    values_pattern = r"\[(.*?)\]"
    values_match = re.search(values_pattern, llm_output)
    
    values = []
    if values_match:
        values_str = values_match.group(1)
        # 
        for val in values_str.split(','):
            val = val.strip()
            try:
                # 
                if '.' in val:
                    values.append(float(val))
                else:
                    values.append(int(val))
            except ValueError:
                # ，
                values.append(val)
    
    return columns, values

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

def process_add_column(table_data: List[List[Any]], new_columns: List[str], new_values: List[Any] = None) -> List[List[Any]]:
    """
    
    
    Args:
        table_data: 
        new_columns: 
        new_values: 
        
    Returns:
        
    """
    if not table_data or len(table_data) < 1:
        return []
        
    # 
    existing_columns = table_data[0]
    
    print("add_column--add_column--add_column--add_column--add_column--add_column--add_column")
    print("new_columns: ", new_columns)
    print("existing_columns: ", existing_columns)
    print("table_data: ", table_data)
    print("new_values: ", new_values)

    # 
    if len(table_data) - 1 != len(new_values):
        return []
    
    # 
    existing_values = [[row[idx] for row in table_data[1:]] for idx in range(len(existing_columns))]
    for values_now in existing_values:
        if values_now == new_values:
            return []
    
    # 
    valid_columns = []
    for col in new_columns:
        if validate_column_name(col, existing_columns):
            valid_columns.append(col)
    
    if not valid_columns:
        return []
    
    # 
    new_table = [row[:] for row in table_data]
    
    # 
    new_table[0].extend(valid_columns)
    
    # 
    for i in range(1, len(new_table)):
        new_table[i].append(new_values[i-1])
    
    return new_table
