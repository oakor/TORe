import json
import pandas as pd
from typing import List, Dict, Any

def convert_to_ftct_format(input_file: str, multi_table: bool = False) -> List[Dict[str, Any]]:
    """
     Ftct 
    
    Args:
        input_file: 
        multi_table: 
    Returns:
        
    """
    # 
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 
    ftct_data = []
    for item in data:
        # instruction
        instruction = item['instruction']
        table_start = instruction.find('##Instruction:')
        if table_start == -1:
            continue
            
        table_json = instruction[table_start + len('##Instruction:'):].strip()
        table_data = json.loads(table_json)
        
        if not multi_table:
            # 
            table_text = []
            
            # 
            table_text.append([str(col) for col in table_data['columns']])
            
            # 
            for row in table_data['data']:
                table_text.append([str(cell) for cell in row])
            
            #  Ftct 
            ftct_item = {
                "id": item['id'],
                "statement": item['input'].replace('###Input:\n', '').replace('\n\n###Response:', ''),
                "table_caption": None,
                "table_info": {
                    "table_text": table_text
                }
            }
            
            ftct_data.append(ftct_item)
        else:
            table_all = []
            table_name = []
            for table in table_data[:-1]:
                table_text = []
                # 
                table_text.append([str(col) for col in table['columns']])
                # 
                for row in table['data']:
                    table_text.append([str(cell) for cell in row])
                table_all.append(table_text)
                table_name.append(table['table_name'])
            
            ftct_item = {
                "id": item['id'],
                "statement": item['input'].replace('###Input:\n', '').replace('\n\n###Response:', ''),
                "table_caption": table_name,
                "table_info": {
                    "table_text": table_all,
                    "foreign_key": table_data[-1].get("foreign_keys")
                }
            }
            ftct_data.append(ftct_item)
    
    return ftct_data

def save_ftct_format(data: List[Dict[str, Any]], output_file: str):
    """
    
    
    Args:
        data: 
        output_file: 
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2) 


if __name__ == "__main__":
    input_file = ""
    output_file = ""
    data = convert_to_ftct_format(input_file, multi_table=True)
    save_ftct_format(data, output_file)