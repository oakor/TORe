import re
from typing import List, Optional

def extract_select_table_params(llm_output: str) -> Optional[str]:
    """LLMf_select_table"""
    match = re.search(r"f_select_table\(([^)]+)\)", llm_output)
    if match:
        return match.group(1).strip()
    return None

def process_select_table(
    tables: List[List[List[str]]], 
    table_names: List[str], 
    table_name: str
) -> Optional[List[List[str]]]:
    """
    
    
    Args:
        tables: 
        table_names: 
        table_name: 
        
    Returns:
        
    """
    try:
        # 
        table_idx = table_names.index(table_name)
        return tables[table_idx]
    except (ValueError, IndexError) as e:
        print(f"Error processing select_table: {e}")
        return None 