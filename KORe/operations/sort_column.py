import re
from typing import List, Any, Tuple, Optional
import copy

def extract_sort_column_params(llm_output: str) -> Tuple[str, str]:
    """
    LLMf_sort_column
    
    Args:
        llm_output: LLM
        
    Returns:
        (, )
    """
    # f_sort_column
    pattern = r"f_sort_column\((.*?)\)"
    match = re.search(pattern, llm_output, re.IGNORECASE)
    
    if not match:
        return "", ""
        
    # 
    params_str = match.group(1).strip()
    
    # 
    order_pattern = r'(?:small to large|large to small)'
    order_match = re.search(order_pattern, params_str, re.IGNORECASE)
    order = "small to large" if order_match and order_match.group(0).lower().startswith('s') else "large to small"
    
    # 
    column = re.sub(order_pattern, '', params_str, flags=re.IGNORECASE).strip()
    column = column.strip('\'"')
    
    return column, order

def get_sort_key(value: Any, col_type: str = "auto") -> Any:
    """
    
    
    Args:
        value: 
        col_type: （"auto", "numeric", "date", "string"）
        
    Returns:
        
    """
    if not value or not str(value).strip():
        return float('-inf') if col_type == "numeric" else ""
        
    value = str(value).strip()
    
    if col_type == "numeric":
        # 
        num_str = ""
        has_dot = False
        is_negative = value.startswith('-')
        
        for c in value:
            if c.isdigit():
                num_str += c
            elif c == '.' and not has_dot:
                num_str += c
                has_dot = True
                
        if not num_str or num_str == '.':
            return float('-inf')
            
        try:
            return float(('-' if is_negative else '') + num_str)
        except ValueError:
            return float('-inf')
            
    elif col_type == "date":
        # 
        try:
            # 
            return value
        except:
            return ""
            
    else:  # string or auto
        return value.lower()

def detect_column_type(values: List[Any]) -> str:
    """
    
    
    Args:
        values: 
        
    Returns:
        （"numeric", "date", "string"）
    """
    numeric_count = 0
    date_count = 0
    total = len(values)
    
    for value in values:
        if not value or not str(value).strip():
            continue
            
        value = str(value).strip()
        
        # 
        try:
            float(value)
            numeric_count += 1
            continue
        except ValueError:
            pass
            
        # 
        if re.match(r'\d{4}[-/]\d{1,2}[-/]\d{1,2}|\d{1,2}[-/]\d{1,2}[-/]\d{4}', value):
            date_count += 1
            continue
    
    # 
    if numeric_count / total > 0.5:
        return "numeric"
    elif date_count / total > 0.5:
        return "date"
    else:
        return "string"

def process_sort_column(table_data: List[List[Any]], sort_column: str, order: str) -> List[List[Any]]:
    """
    
    
    Args:
        table_data: 
        sort_column: 
        order: 
        
    Returns:
        
    """
    if not table_data or len(table_data) < 2:
        return table_data
        
    # 
    try:
        header = table_data[0]
        col_index = header.index(sort_column.lower())
    except ValueError:
        return table_data
    
    # 
    header = table_data[0]
    data = table_data[1:]
    
    # 
    col_values = [row[col_index] for row in data]
    col_type = detect_column_type(col_values)
    
    # 
    reverse = order.lower() == "large to small"
    sorted_data = sorted(
        data,
        key=lambda row: get_sort_key(row[col_index], col_type),
        reverse=reverse
    )
    
    # 
    return [header] + sorted_data 



if __name__ == '__main__':
    p = """ The existing columns are: Group, Members, Caucusing.
Explanation: The question wants to know the total number of caucusing members in groups that have more than 100 members. We need to know the order of the groups by the number of members from the most to the least. There is a column for members and the column name is members. The datatype is Numerical.
Therefore, the answer is: f_sort_column(Members), the order is "large to small". Then we can count the number of caucusing members in groups that have more than 100 members.
New Table:
/*
col : Group | Members | Caucusing |
row 1 : Socialist Group | 242 | 8 |
row 2 : RPR Group | 136 | 6 |
row 3 : UDF Group | 107 | 6 |
*/"""
    t1, t2 = extract_sort_column_params(p)

    table_info = [['Group', 'Members', 'Caucusing'], ['Socialist Group', 242, 8], ['RPR Group', 136, 6], ['UDF Group', 107, 6], ['Communist Group', 34, 2], ['Radical, Citizen and Green', 33, 0], ['Non-Inscrits', 5, 0], ['Total:', 555, 22]]
    new_tables = process_sort_column(table_info, t1, t2)
    print(new_tables)