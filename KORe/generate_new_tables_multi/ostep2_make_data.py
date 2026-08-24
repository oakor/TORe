import os
import json
import logging
from typing import List, Dict, Any
import sys
from vllm import LLM, SamplingParams
from tqdm import tqdm
import random
import torch
import itertools
import argparse
from importlib import import_module

task_ID_debug_path = ""
# debug
def save_debug_info(data, filename=task_ID_debug_path):
    """
    debug
    
    Args:
        data: 
        filename: 
    """
    try:
        # ，
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                try:
                    existing_data = json.load(f)
                except:
                    existing_data = []
        else:
            existing_data = []
        
        # 
        if isinstance(existing_data, list):
            existing_data.append(data)
        else:
            existing_data = [existing_data, data]
        
        # 
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logging.error(f"debug: {str(e)}")

from prompts import generate_chain_param_prompt, generate_qa_prompt
from prompts import f_add_knowledge_column_demos, f_add_inferred_column_demos

sys.path.append("..")
from utils import convert_to_ftct_format

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from operations.add_knowledge_column import process_add_knowledge_column
from operations.add_inferred_column import process_add_inferred_column
from operations.sort_column import process_sort_column
from operations.select_column import process_select_column
from operations.select_row import process_select_row
from operations.group_column import process_group_column
from operations.stitch_tables import process_stitch_tables
from operations.change_column_name import process_change_column_name
from operations.select_table import process_select_table

# 
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

task_ID = 0

def generate_table_prompt(table_text: List[List[str]], is_multi_table: bool = False, table_names: List[str] = None, foreign_key: str = None) -> str: 
    """
    
    
    Args:
        table_text: ，
        is_multi_table: 
        table_names: 
        foreign_key: 
        
    Returns:
        
    """
    prompt = ""
    
    print("table_text: ", table_text)
    print("is_multi_table: ", is_multi_table)
    print("table_names: ", table_names)
    print("foreign_key: ", foreign_key)
    if is_multi_table and isinstance(table_text[0], list) and isinstance(table_text[0][0], list):
        # 
        prompt += "/*\n"
        for i, table in enumerate(table_text):
            table_name = table_names[i] if table_names and i < len(table_names) else f"table_{i}"
            prompt += f"table_name: {table_name}\n"
            prompt += "col : " + " | ".join([str(item) for item in table[0]]) + "\n"
            for idx, row in enumerate(table[1:], 1):
                prompt += f"row {idx} : " + " | ".join([str(item) for item in row]) + "\n"
            prompt += "\n"
        
        # 
        if foreign_key:
            prompt += f"foreign_key: {foreign_key}\n"
        prompt += "*/\n"
    else:
        # 
        prompt += "/*\n"
        prompt += "col : " + " | ".join([str(item) for item in table_text[0]]) + "\n"
        for idx, row in enumerate(table_text[1:], 1):
            prompt += "row " + str(idx) + " : " + " | ".join([str(item) for item in row]) + "\n"
        prompt += "*/\n"
    
    return prompt

def chat(llm, sampling_params, prompts, system_prompt, using_prefix_caching=False):
    """
    
    
    Args:
        llm: 
        sampling_params: 
        prompts: 
        system_prompt: 
        using_prefix_caching: 
        
    Returns:
        ，sampling_params.n > 1，
    """
    messages = []
    for prompt in prompts:
        message = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user", 
                "content": prompt
            },
        ]
        messages.append(message)
    
    # 
    debug_input = {
        "type": "llm_input",
        "timestamp": str(import_module('datetime').datetime.now()),
        "prompts": prompts,
        "system_prompt": system_prompt,
        "sampling_params": {
            "temperature": getattr(sampling_params, "temperature", None),
            "top_p": getattr(sampling_params, "top_p", None),
            "max_tokens": getattr(sampling_params, "max_tokens", None),
            "n": getattr(sampling_params, "n", None)
        },
        "using_prefix_caching": using_prefix_caching
    }
    save_debug_info(debug_input)
    
    # ，llm
    original_prefix_caching = None
    if using_prefix_caching:
        if hasattr(llm, 'prefix_caching'):
            original_prefix_caching = getattr(llm, 'prefix_caching', None)
            llm.prefix_caching = True
        elif hasattr(llm, 'enable_prefix_caching'):
            original_prefix_caching = getattr(llm, 'enable_prefix_caching', None)
            llm.enable_prefix_caching = True
    
    outputs = llm.chat(messages,
                    sampling_params=sampling_params,
                    use_tqdm=True)
                    
    # llm
    if using_prefix_caching and original_prefix_caching is not None:
        if hasattr(llm, 'prefix_caching'):
            llm.prefix_caching = original_prefix_caching
        elif hasattr(llm, 'enable_prefix_caching'):
            llm.enable_prefix_caching = original_prefix_caching
    
    generated_texts = []
    # （n > 1）
    if hasattr(sampling_params, 'n') and sampling_params.n > 1:
        for output in outputs:
            prompt_results = []
            for out in output.outputs:
                text = out.text.split("<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n")[0]
                prompt_results.append(text)
            generated_texts.append(prompt_results)
    else:
        for output in outputs:
            generated_text = output.outputs[0].text
            generated_texts.append(generated_text.split("<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n")[0])
    
    # 
    debug_output = {
        "type": "llm_output",
        "timestamp": str(import_module('datetime').datetime.now()),
        "generated_texts": generated_texts
    }
    save_debug_info(debug_output)
    
    return generated_texts

def process_table_with_chain(table: List[List[Any]], chain: List[str], llm, sampling_params, is_multi_table: bool = False, table_names: List[str] = None, foreign_key: str = None) -> List[List[Any]]:
    """
    
    
    Args:
        table: 
        chain: 
        llm: 
        sampling_params: 
        is_multi_table: 
        table_names: 
        foreign_key: 
        
    Returns:
        
    """
    current_table = table.copy()
    # 
    table_str = generate_table_prompt(current_table, is_multi_table=is_multi_table, table_names=table_names, foreign_key=foreign_key)
    
    # 
    chain_param_prompt = generate_chain_param_prompt(
        table_info=table_str,
        chain=chain,
        task_id=task_ID,
        random_seed=random.randint(1, 100),
        is_multi_table=is_multi_table
    )
    chain_param_response = chat(llm, sampling_params, [chain_param_prompt], "")[0]
    # 
    operations = []
    explanations = []
    for line in chain_param_response.split('\n'):
        if line.startswith('Operation'):
            op = line.split(':')[1].strip()
            operations.append(op)
        elif line.startswith('Explanation'):
            explanation = line.split(':')[1].strip()
            explanations.append(explanation)
    # 
    def safe_eval_list_string(input_str: str) -> List[Any]:
        """
        ，
        
        Args:
            input_str: ， "1,2,3"  "Sitcom, Sitcom, Sitcom"
            
        Returns:
            ，intfloat
        """
        try:
            # 
            input_str = input_str.strip()
            
            # ，
            if input_str.startswith('[') and input_str.endswith(']'):
                input_str = input_str[1:-1]
                
            # 
            items = []
            for item in input_str.split(','):
                item = item.strip().strip('"\'')  # 
                if not item:  # 
                    continue
                    
                # 
                try:
                    if '.' in item:  # 
                        items.append(float(item))
                    else:  # 
                        items.append(int(item))
                except ValueError:  # ，
                    items.append(item)
            
            return items
        except Exception as e:
            logger.error(f": {str(e)}")
            return []
        
    def get_valid_table_response(llm, sampling_params, values_prompt, table, col_name, process_func):
        """
        
        
        Args:
            llm: 
            sampling_params: 
            values_prompt: 
            table: 
            col_name: 
            process_func: （process_add_knowledge_column  process_add_inferred_column）
            
        Returns:
            ，None
        """
        # ，3
        new_sampling_params = SamplingParams(
            temperature=0.7,  # temperature
            top_p=0.95,
            max_tokens=sampling_params.max_tokens,
            n=3  # 3
        )
        values_responses = chat(llm, new_sampling_params, [values_prompt], "")
        
        # chat，values_responses[0]
        if len(values_responses) > 0 and isinstance(values_responses[0], list):
            responses_to_process = values_responses[0]
        else:
            # 
            responses_to_process = values_responses
        
        for values_response in responses_to_process:
            try:
                # values
                values_str = values_response.split('[')[1].split(']')[0]
                values = safe_eval_list_string(values_str)
                
                # 
                current_table = process_func(table, [col_name], values)
                
                # ，
                if current_table and len(current_table) > 0:
                    return current_table, values
            except Exception as e:
                logger.error(f": {str(e)}")
                continue
        
        return None, None
    try:
        for op, explanation in zip(operations, explanations):
            if op.startswith('f_add_knowledge_column'):
                # 
                col_name = op.split('(')[1].split(')')[0].strip()
                # values
                values_prompt = f_add_knowledge_column_demos.replace("[Insert Table Here]", table_str).replace("[Insert Function Here]", op).replace("[Insert Explanation Here]", explanation)
                # 
                current_table, values = get_valid_table_response(
                    llm, 
                    sampling_params, 
                    values_prompt, 
                    current_table, 
                    col_name, 
                    process_add_knowledge_column
                )
                if current_table is None:
                    logger.error("，")
                    continue
                # values
            elif op.startswith('f_add_inferred_column'):
                col_name = op.split('(')[1].split(')')[0].strip()
                values_prompt = f_add_inferred_column_demos.replace("[Insert Table Here]", table_str).replace("[Insert Function Here]", op).replace("[Insert Explanation Here]", explanation)
                current_table, values = get_valid_table_response(
                    llm, 
                    sampling_params, 
                    values_prompt, 
                    current_table, 
                    col_name, 
                    process_add_inferred_column
                )
                if current_table is None:
                    logger.error("，")
                    continue
            elif op.startswith('f_sort_column'):
                col_name = op.split('(')[1].split(')')[0].strip()
                orders = ["small to large", "large to small"]
                order = random.choice(orders)
                current_table = process_sort_column(current_table, col_name, order)
            elif op.startswith('f_select_column'):
                cols = op.split('(')[1].split(')')[0].strip().split(',')
                cols = [col.strip() for col in cols]
                current_table = process_select_column(current_table, cols)
            elif op.startswith('f_select_row'):
                rows = op.split('(')[1].split(')')[0].strip().split(',')
                rows = [int(row.strip().split(' ')[-1]) for row in rows]
                current_table = process_select_row(current_table, rows)
            elif op.startswith('f_group_column'):
                col_name = op.split('(')[1].split(')')[0].strip().split(',')
                current_table = process_group_column(current_table, col_name)
            elif op.startswith('f_stitch_tables'):
                # 
                if is_multi_table:
                    # 
                    params_str = op.split('(')[1].split(')')[0].strip()
                    params_parts = params_str.split(',')
                    if len(params_parts) >= 3:
                        # ：table1.column1, table2.column2, join_method
                        table1_col = params_parts[0].strip()
                        table2_col = params_parts[1].strip()
                        join_method = params_parts[2].strip().strip('"\'')
                        
                        # 
                        table_names = []
                        if table_names and table_idx < len(table_names):
                            table_names = table_names[table_idx]
                            # ，
                            if isinstance(table_names, list) and table_names and isinstance(table_names[0], list):
                                table_names = table_names[0]
                        else:
                            # ，
                            table_names = [f"table_{i}" for i in range(len(current_table))]
                        
                        # stitch_tables
                        debug_stitch_tables_input = {
                            "type": "stitch_tables_input",
                            "timestamp": str(import_module('datetime').datetime.now()),
                            "table_idx": table_idx,
                            "table1_col": table1_col,
                            "table2_col": table2_col,
                            "join_method": join_method,
                            "table_names": table_names,
                            "sample_table": str(current_table) if current_table and len(current_table) > 0 else None
                        }
                        save_debug_info(debug_stitch_tables_input)
                        
                        # stitch_tables
                        result_table = process_stitch_tables(
                            current_table, 
                            table_names, 
                            (table1_col, table2_col), 
                            join_method
                        )
                        
                        # stitch_tables
                        debug_stitch_tables_output = {
                            "type": "stitch_tables_output",
                            "timestamp": str(import_module('datetime').datetime.now()),
                            "table_idx": table_idx,
                            "success": result_table is not None,
                            "sample_result": str(result_table[0][:3]) if result_table and len(result_table) > 0 else None
                        }
                        save_debug_info(debug_stitch_tables_output)
                        
                        if result_table:
                            current_table = result_table
                            
                            # 
                            filled_chain = {
                                'operation': op,
                                'explanation': explanation,
                                'params': {
                                    'table1_col': table1_col,
                                    'table2_col': table2_col,
                                    'join_method': join_method
                                }
                            }
                            step_results[table_idx]['filled_chains'].append(filled_chain)
                            step_results[table_idx]['intermediate_tables'].append(current_table.copy())
                        else:
                            logger.error(f" {table_idx} ")
                    else:
                        logger.error(f" {table_idx} ，")
                
                # ，
                op_indices[table_idx] += 1
                continue
                
            elif op.startswith('f_select_table'):
                # 
                if is_multi_table:
                    # 
                    table_name = op.split('(')[1].split(')')[0].strip().strip('"\'')
                    
                    # 
                    table_names = []
                    if table_names and table_idx < len(table_names):
                        table_names = table_names[table_idx]
                        # ，
                        if isinstance(table_names, list) and table_names and isinstance(table_names[0], list):
                            table_names = table_names[0]
                    else:
                        # ，
                        table_names = [f"table_{i}" for i in range(len(current_table))]
                    
                    # select_table
                    debug_select_table_input = {
                        "type": "select_table_input",
                        "timestamp": str(import_module('datetime').datetime.now()),
                        "table_idx": table_idx,
                        "table_name": table_name,
                        "table_names": table_names,
                        "sample_table": str(current_table) if current_table and len(current_table) > 0 else None
                    }
                    save_debug_info(debug_select_table_input)
                    
                    # select_table
                    result_table = process_select_table(
                        current_table, 
                        table_names, 
                        table_name
                    )
                    
                    # select_table
                    debug_select_table_output = {
                        "type": "select_table_output",
                        "timestamp": str(import_module('datetime').datetime.now()),
                        "table_idx": table_idx,
                        "success": result_table is not None,
                        "sample_result": str(result_table[0][:3]) if result_table and len(result_table) > 0 else None
                    }
                    save_debug_info(debug_select_table_output)
                    
                    if result_table:
                        current_table = result_table
                        
                        # 
                        filled_chain = {
                            'operation': op,
                            'explanation': explanation,
                            'params': {
                                'table_name': table_name
                            }
                        }
                        step_results[table_idx]['filled_chains'].append(filled_chain)
                        step_results[table_idx]['intermediate_tables'].append(current_table.copy())
                    else:
                        logger.error(f" {table_idx} ")
                else:
                    logger.error(f" {table_idx} ，")
                
                # ，
                op_indices[table_idx] += 1
                continue
            elif op.startswith('f_change_column_name'):
                old_name, new_name = op.split('(')[1].split(')')[0].strip().split(',')
                old_name = old_name.strip().strip('"')
                new_name = new_name.strip().strip('"')
                current_table = process_change_column_name(current_table, old_name, new_name)
    except:
        print("cannot got right output, so skip")
        return []
    return current_table

# def generate_qa_pairs(table: List[List[Any]], chain: List[str], llm, sampling_params, table_id: str = None) -> Dict[str, Any]:
#     """
#     
    
#     Args:
#         table: 
#         chain: 
#         llm: 
#         sampling_params: 
#         table_id: ID
        
#     Returns:
#         
#     """
#     # 
#     table_str = generate_table_prompt(table)
#     processed_table = process_table_with_chain(table, chain, llm, sampling_params)
#     if not processed_table:
#         return None
    
#     # 
#     qa_prompt = generate_qa_prompt(
#         original_table=table_str,
#         chain_with_params=chain,
#         final_table=generate_table_prompt(processed_table)
#     )
#     qa_response = chat(llm, sampling_params, [qa_prompt], "")[0]
    
#     # 
#     question = qa_response.split('Question:')[1].split('Answer:')[0].strip()
#     answer = qa_response.split('Answer:')[1].split('Explanation:')[0].strip()
#     explanation = qa_response.split('Explanation:')[1].strip()
    
#     result = {
#         'question': question,
#         'answer': answer,
#         'explanation': explanation,
#         'table': processed_table,
#         'chain': chain
#     }
    
#     # table_id，id
#     if table_id is not None:
#         result['id'] = table_id
        
#     return result

def generate_chain_params_batch(tables: List[List[List[Any]]], chains: List[List[str]], llm: LLM, sampling_params: SamplingParams, is_multi_table: bool = False, table_captions: List[str] = None, foreign_keys: List[str] = None) -> List[Dict[str, Any]]:
    """
    
    
    Args:
        tables: 
        chains: 
        llm: 
        sampling_params: 
        is_multi_table: 
        table_captions: 
        foreign_keys: 
        
    Returns:
        
    """
    # 
    prompts = []
    #random_seed = random.randint(1, 100)
    for i, (table, chain) in enumerate(zip(tables, chains)):
        random_seed = random.randint(1, 100)
        # 
        table_name = table_captions[i] if table_captions and i < len(table_captions) else None
        foreign_key = foreign_keys[i] if foreign_keys and i < len(foreign_keys) else None
        
        # 
        table_str = generate_table_prompt(table, is_multi_table=is_multi_table, table_names=table_name, foreign_key=foreign_key)
        chain_param_prompt = generate_chain_param_prompt(
            table_info=table_str,
            chain=chain,
            task_id=task_ID,
            random_seed=random_seed,
            is_multi_table=is_multi_table
        )
        prompts.append(chain_param_prompt)
    
    # 
    debug_chain_params_input = {
        "type": "chain_params_input",
        "timestamp": str(import_module('datetime').datetime.now()),
        "num_tables": len(tables),
        "num_chains": len(chains),
        "is_multi_table": is_multi_table,
        "sample_prompt": prompts[0][:200] if prompts else None
    }
    save_debug_info(debug_chain_params_input)
    
    # 
    sampling_params = SamplingParams(temperature=0, top_p=0.95, max_tokens=4096)
    responses = chat(llm, sampling_params, prompts, "", using_prefix_caching=False)
    
    # 
    results = []
    for response in responses:
        with open("chain_params.txt", "a", encoding="utf-8") as fp:
            fp.write(response + "\n-------------------------------------------------------------------------\n\n\n\n\n\n")
        operations = []
        explanations = []
        for line in response.split('\n'):
            if line.startswith('Operation'):
                try:
                    op = line.split(':')[1].strip()
                except:
                    continue
                operations.append(op)
            elif line.startswith('Explanation'):
                try:
                    explanation = line.split(':')[1].strip()
                except:
                    continue
                explanations.append(explanation)
        if len(operations) != len(explanations):
            logger.error(f": {len(operations)} != {len(explanations)}")
            explanations = explanations[:len(operations)] if len(operations) < len(explanations) else explanations + [""] * (len(operations) - len(explanations))
        results.append({
            'operations': operations,
            'explanations': explanations
        })
    
    # 
    debug_chain_params_output = {
        "type": "chain_params_output",
        "timestamp": str(import_module('datetime').datetime.now()),
        "num_results": len(results),
        "sample_operations": results[0]['operations'] if results else None
    }
    save_debug_info(debug_chain_params_output)
    
    return results

def process_tables_with_params(tables: List[List[List[Any]]], chains: List[List[str]], params_list: List[Dict[str, Any]], llm: LLM, sampling_params: SamplingParams, is_multi_table: bool = False, table_captions: List[str] = None, foreign_keys: List[str] = None) -> List[Dict[str, Any]]:
    """
    
    
    Args:
        tables: 
        chains: 
        params_list: 
        llm: 
        sampling_params: 
        is_multi_table: 
        table_captions: 
        foreign_keys: 
        
    Returns:
        
    """
    def safe_eval_list_string(input_str: str) -> List[Any]:
        """
        ，
        
        Args:
            input_str: ， "1,2,3"  "Sitcom, Sitcom, Sitcom"
            
        Returns:
            ，intfloat
        """
        try:
            # 
            input_str = input_str.strip()
            
            # ，
            if input_str.startswith('[') and input_str.endswith(']'):
                input_str = input_str[1:-1]
                
            # 
            items = []
            for item in input_str.split(','):
                item = item.strip().strip('"\'')  # 
                if not item:  # 
                    continue
                    
                # 
                try:
                    if '.' in item:  # 
                        items.append(float(item))
                    else:  # 
                        items.append(int(item))
                except ValueError:  # ，
                    items.append(item)
            
            return items
        except Exception as e:
            logger.error(f": {str(e)}")
            return []

    # 
    processed_results = []
    current_tables = [table.copy() for table in tables]
    
    # 
    op_indices = [0] * len(tables)
    
    # 
    completed = [False] * len(tables)
    
    # 
    step_results = [{
        'final_table': None,
        'filled_chains': [],
        'intermediate_tables': [table.copy()]
    } for table in tables]
    
    # ，
    while not all(completed):
        # 
        knowledge_prompts = []
        knowledge_info = []  # [(table_idx, op_idx, col_name), ...]
        
        # 
        inferred_prompts = []
        inferred_info = []  # [(table_idx, op_idx, col_name), ...]
        
        # ：LLM
        for table_idx in range(len(tables)):
            # 
            if completed[table_idx]:
                continue
            
            # 
            current_op_idx = op_indices[table_idx]
            params = params_list[table_idx]
            
            # 
            if current_op_idx >= len(params['operations']):
                completed[table_idx] = True
                continue
            
            # 
            op = params['operations'][current_op_idx]
            explanation = params['explanations'][current_op_idx]
            
            # 
            try:
                # ，
                if is_multi_table and isinstance(current_tables[table_idx], list) and len(current_tables[table_idx]) > 0 and isinstance(current_tables[table_idx][0], list) and isinstance(current_tables[table_idx][0][0], list):
                    # ，
                    table_name = table_captions[table_idx] if table_captions and table_idx < len(table_captions) else f"table_{table_idx}"
                    foreign_key = foreign_keys[table_idx] if foreign_keys and table_idx < len(foreign_keys) else None
                    
                    table_str = generate_table_prompt(current_tables[table_idx], is_multi_table=True, table_names=[table_name], foreign_key=foreign_key)
                else:
                    # 
                    table_str = generate_table_prompt(current_tables[table_idx], is_multi_table=False)
            except Exception as e:
                logger.error(f" {table_idx} : {str(e)}")
                completed[table_idx] = True
                continue
            
            # 
            try:
                if op.startswith('f_add_knowledge_column'):
                    # 
                    col_name = op.split('(')[1].split(')')[0].strip()
                    values_prompt = f_add_knowledge_column_demos.replace("[Insert Table Here]", table_str).replace("[Insert Function Here]", op).replace("[Insert Explanation Here]", explanation)
                    knowledge_prompts.append(values_prompt)
                    knowledge_info.append((table_idx, current_op_idx, col_name))
                    
                    # ，
                    continue
                    
                elif op.startswith('f_add_inferred_column'):
                    # 
                    col_name = op.split('(')[1].split(')')[0].strip()
                    values_prompt = f_add_inferred_column_demos.replace("[Insert Table Here]", table_str).replace("[Insert Function Here]", op).replace("[Insert Explanation Here]", explanation)
                    inferred_prompts.append(values_prompt)
                    inferred_info.append((table_idx, current_op_idx, col_name))
                    
                    # ，
                    continue
                    
                elif op.startswith('f_stitch_tables'):
                    # 
                    if is_multi_table:
                        # 
                        params_str = op.split('(')[1].split(')')[0].strip()
                        params_parts = params_str.split(',')
                        if len(params_parts) >= 3:
                            # ：table1.column1, table2.column2, join_method
                            table1_col = params_parts[0].strip()
                            table2_col = params_parts[1].strip()
                            join_method = params_parts[2].strip().strip('"\'')
                            
                            # 
                            table_names = []
                            if table_captions and table_idx < len(table_captions):
                                table_names = table_captions[table_idx]
                                # ，
                                if isinstance(table_names, list) and table_names and isinstance(table_names[0], list):
                                    table_names = table_names[0]
                            else:
                                # ，
                                table_names = [f"table_{i}" for i in range(len(current_tables[table_idx]))]
                            

                            # stitch_tables
                            debug_stitch_tables_input = {
                                "type": "stitch_tables_input",
                                "timestamp": str(import_module('datetime').datetime.now()),
                                "table_idx": table_idx,
                                "table1_col": table1_col,
                                "table2_col": table2_col,
                                "join_method": join_method,
                                "table_names": table_names,
                                "sample_table": str(current_tables[table_idx]) if current_tables[table_idx] and len(current_tables[table_idx]) > 0 else None
                            }
                            save_debug_info(debug_stitch_tables_input)
                            
                            # stitch_tables
                            result_table = process_stitch_tables(
                                current_tables[table_idx], 
                                table_names, 
                                (table1_col, table2_col), 
                                join_method
                            )
                            
                            # stitch_tables
                            debug_stitch_tables_output = {
                                "type": "stitch_tables_output",
                                "timestamp": str(import_module('datetime').datetime.now()),
                                "table_idx": table_idx,
                                "success": result_table is not None,
                                "sample_result": str(result_table[0][:3]) if result_table and len(result_table) > 0 else None
                            }
                            save_debug_info(debug_stitch_tables_output)
                            
                            if result_table:
                                current_tables[table_idx] = result_table
                                print("--------------------------------")
                                print(f" {table_idx} ")
                                print("current_table: ", current_tables[table_idx])
                                print("--------------------------------")
                                
                                # 
                                filled_chain = {
                                    'operation': op,
                                    'explanation': explanation,
                                    'params': {
                                        'table1_col': table1_col,
                                        'table2_col': table2_col,
                                        'join_method': join_method
                                    }
                                }
                                step_results[table_idx]['filled_chains'].append(filled_chain)
                                step_results[table_idx]['intermediate_tables'].append(current_tables[table_idx].copy())
                            else:
                                logger.error(f" {table_idx} ")
                        else:
                            logger.error(f" {table_idx} ")
                    else:
                        logger.error(f" {table_idx} ，")
                    
                    # ，
                    op_indices[table_idx] += 1
                    continue
                    
                elif op.startswith('f_select_table'):
                    # 
                    if is_multi_table:
                        # 
                        table_name = op.split('(')[1].split(')')[0].strip().strip('"\'')
                        
                        # 
                        table_names = []
                        if table_captions and table_idx < len(table_captions):
                            table_names = table_captions[table_idx]
                            # ，
                            if isinstance(table_names, list) and table_names and isinstance(table_names[0], list):
                                table_names = table_names[0]
                        else:
                            # ，
                            table_names = [f"table_{i}" for i in range(len(current_tables[table_idx]))]
                        

                        # select_table
                        debug_select_table_input = {
                            "type": "select_table_input",
                            "timestamp": str(import_module('datetime').datetime.now()),
                            "table_idx": table_idx,
                            "table_name": table_name,
                            "table_names": table_names,
                            "sample_table": str(current_tables[table_idx]) if current_tables[table_idx] and len(current_tables[table_idx]) > 0 else None
                        }
                        save_debug_info(debug_select_table_input)
                        
                        # select_table
                        result_table = process_select_table(
                            current_tables[table_idx], 
                            table_names, 
                            table_name
                        )
                        
                        # select_table
                        debug_select_table_output = {
                            "type": "select_table_output",
                            "timestamp": str(import_module('datetime').datetime.now()),
                            "table_idx": table_idx,
                            "success": result_table is not None,
                            "sample_result": str(result_table[0][:3]) if result_table and len(result_table) > 0 else None
                        }
                        save_debug_info(debug_select_table_output)
                        
                        if result_table:
                            current_tables[table_idx] = result_table
                            print("--------------------------------")
                            print(f" {table_idx} ")
                            print("current_table: ", current_tables[table_idx])
                            print("--------------------------------")
                            
                            # 
                            filled_chain = {
                                'operation': op,
                                'explanation': explanation,
                                'params': {
                                    'table_name': table_name
                                }
                            }
                            step_results[table_idx]['filled_chains'].append(filled_chain)
                            step_results[table_idx]['intermediate_tables'].append(current_tables[table_idx].copy())
                        else:
                            logger.error(f" {table_idx} ")
                    else:
                        logger.error(f" {table_idx} ，")
                    
                    # ，
                    op_indices[table_idx] += 1
                    continue
            except Exception as e:
                logger.error(f" {table_idx}  {op} : {str(e)}")
                completed[table_idx] = True
                continue
                
            # LLM
            try:
                if op.startswith('f_sort_column'):
                    col_name = op.split('(')[1].split(')')[0].strip()
                    orders = ["small to large", "large to small"]
                    order = random.choice(orders)
                    current_tables[table_idx] = process_sort_column(current_tables[table_idx], col_name, order)
                    print("--------------------------------")
                    print("op: ", op)
                    print("current_table: ", current_tables[table_idx])
                    print("--------------------------------")
                    
                elif op.startswith('f_select_column'):
                    cols = op.split('(')[1].split(')')[0].strip().split(',')
                    cols = [col.strip() for col in cols]
                    current_tables[table_idx] = process_select_column(current_tables[table_idx], cols)
                    print("--------------------------------")
                    print("op: ", op)
                    print("current_table: ", current_tables[table_idx])
                    print("--------------------------------")
                    
                elif op.startswith('f_select_row'):
                    rows = op.split('(')[1].split(')')[0].strip().split(',')
                    rows = [int(row.strip().split(' ')[-1]) for row in rows]
                    current_tables[table_idx] = process_select_row(current_tables[table_idx], rows)
                    print("--------------------------------")
                    print("op: ", op)
                    print("current_table: ", current_tables[table_idx])
                    print("--------------------------------")
                    
                elif op.startswith('f_group_column'):
                    col_name = op.split('(')[1].split(')')[0].strip().split(',')
                    current_tables[table_idx] = process_group_column(current_tables[table_idx], col_name)
                    print("--------------------------------")
                    print("op: ", op)
                    print("current_table: ", current_tables[table_idx])
                    print("--------------------------------")
                    
                elif op.startswith('f_change_column_name'):
                    old_name, new_name = op.split('(')[1].split(')')[0].strip().split(',')
                    old_name = old_name.strip().strip('"')
                    new_name = new_name.strip().strip('"')
                    current_tables[table_idx] = process_change_column_name(current_tables[table_idx], old_name, new_name)
                    print("--------------------------------")
                    print("op: ", op)
                    print("current_table: ", current_tables[table_idx])
                    print("--------------------------------")
                
                # 
                filled_chain = {
                    'operation': op,
                    'explanation': explanation
                }
                step_results[table_idx]['filled_chains'].append(filled_chain)
                step_results[table_idx]['intermediate_tables'].append(current_tables[table_idx].copy())
                
                # ，
                op_indices[table_idx] += 1
                
            except Exception as e:
                logger.error(f" {table_idx}  {op} : {str(e)}")
                completed[table_idx] = True
        
        # ：LLM
        # 
        if knowledge_prompts:
            # ，3
            new_sampling_params = SamplingParams(
                temperature=0.7,
                top_p=0.95,
                max_tokens=sampling_params.max_tokens,
                n=3
            )
            
            # LLM
            knowledge_responses = chat(llm, new_sampling_params, knowledge_prompts, "")
            
            # 
            for i, (table_idx, op_idx, col_name) in enumerate(knowledge_info):
                success = False
                
                # knowledge_responses[i]
                responses_to_process = []
                if i < len(knowledge_responses):
                    if isinstance(knowledge_responses[i], list):
                        responses_to_process = knowledge_responses[i]
                    else:
                        responses_to_process = [knowledge_responses[i]]
                
                for response in responses_to_process:
                    try:
                        # values
                        values_str = response.split('[')[1].split(']')[0]
                        values = safe_eval_list_string(values_str)
                        
                        # 
                        updated_table = process_add_knowledge_column(current_tables[table_idx], [col_name], values)
                        
                        # 
                        if updated_table and len(updated_table) > 0:
                            current_tables[table_idx] = updated_table
                            success = True
                            print("--------------------------------")
                            print(f" {table_idx}  {col_name} ")
                            print("values: ", values)
                            print("current_table: ", current_tables[table_idx])
                            print("--------------------------------")
                            
                            # 
                            filled_chain = {
                                'operation': f"f_add_knowledge_column({col_name})",
                                'explanation': params_list[table_idx]['explanations'][op_idx],
                                'values': values
                            }
                            step_results[table_idx]['filled_chains'].append(filled_chain)
                            step_results[table_idx]['intermediate_tables'].append(current_tables[table_idx].copy())
                            
                            break
                    except Exception as e:
                        with open("knowledge_error.txt", "a", encoding="utf-8") as fp:
                            for i in range(len(responses_to_process)):
                                fp.write(f"response {i}: {responses_to_process[i]}\n-------------------------------------------------------------------------\n\n\n\n\n\n")
                        logger.error(f" {table_idx}  {col_name} : {str(e)}")
                        continue
                
                if not success:
                    with open("knowledge_error.txt", "a", encoding="utf-8") as fp:
                        for i in range(len(responses_to_process)):
                            fp.write(f"response {i}: {responses_to_process[i]}\n-------------------------------------------------------------------------\n\n\n\n\n\n")
                    logger.error(f" {table_idx}  {col_name} ")
                
                # ，
                op_indices[table_idx] += 1
        
        # 
        if inferred_prompts:
            # ，3
            new_sampling_params = SamplingParams(
                temperature=0.7,
                top_p=0.95,
                max_tokens=sampling_params.max_tokens,
                n=3
            )
            
            # LLM
            inferred_responses = chat(llm, new_sampling_params, inferred_prompts, "")
            
            # 
            for i, (table_idx, op_idx, col_name) in enumerate(inferred_info):
                success = False
                
                # inferred_responses[i]
                responses_to_process = []
                if i < len(inferred_responses):
                    if isinstance(inferred_responses[i], list):
                        responses_to_process = inferred_responses[i]
                    else:
                        responses_to_process = [inferred_responses[i]]
                
                for response in responses_to_process:
                    try:
                        # values
                        values_str = response.split('[')[1].split(']')[0]
                        values = safe_eval_list_string(values_str)
                        
                        # 
                        updated_table = process_add_inferred_column(current_tables[table_idx], [col_name], values)
                        
                        # 
                        if updated_table and len(updated_table) > 0:
                            current_tables[table_idx] = updated_table
                            success = True
                            print("--------------------------------")
                            print(f" {table_idx}  {col_name} ")
                            print("values: ", values)
                            print("current_table: ", current_tables[table_idx])
                            print("--------------------------------")
                            
                            # 
                            filled_chain = {
                                'operation': f"f_add_inferred_column({col_name})",
                                'explanation': params_list[table_idx]['explanations'][op_idx],
                                'values': values
                            }
                            step_results[table_idx]['filled_chains'].append(filled_chain)
                            step_results[table_idx]['intermediate_tables'].append(current_tables[table_idx].copy())
                            
                            break
                    except Exception as e:
                        logger.error(f" {table_idx}  {col_name} : {str(e)}")
                        continue
                
                if not success:
                    with open("inferred_error.txt", "a", encoding="utf-8") as fp:
                        for i in range(len(responses_to_process)):
                            fp.write(f"response {i}: {responses_to_process[i]}\n-------------------------------------------------------------------------\n\n\n\n\n\n")
                    logger.error(f" {table_idx}  {col_name} ")
                
                # ，
                op_indices[table_idx] += 1
        
        # 
        if not knowledge_prompts and not inferred_prompts and not any(not completed[i] and op_indices[i] < len(params_list[i]['operations']) for i in range(len(tables))):
            # ，
            # 
            for i in range(len(completed)):
                if not completed[i]:
                    completed[i] = True
    
    # ，
    for i, table in enumerate(current_tables):
        step_results[i]['final_table'] = table
        processed_results.append(step_results[i])
    
    # filled_chains，1chains1，None
    for i, result in enumerate(processed_results):
        filled_chains_length = len(result['filled_chains'])
        
        # filled_chains1chains1，
        if filled_chains_length <= 1 and i < len(chains) and len(chains[i]) > 1:
            logger.warning(f" {i} filled_chains {filled_chains_length}，chains {len(chains[i])}，")
            processed_results[i]['final_table'] = None
    
    return processed_results

def generate_qa_prompts_batch(original_tables: List[List[List[Any]]], 
                            processed_results: List[Dict[str, Any]], 
                            chains: List[List[str]], 
                            is_multi_table: bool = False,
                            table_captions: List[str] = None,
                            foreign_keys: List[str] = None) -> List[str]:
    """
    
    
    Args:
        original_tables: 
        processed_results: ，final_tablefilled_chains
        chains: 
        is_multi_table: 
        table_captions: 
        foreign_keys: 
        
    Returns:
        
    """
    # generate_qa_prompts_batch
    debug_qa_prompts_input = {
        "type": "qa_prompts_input",
        "timestamp": str(import_module('datetime').datetime.now()),
        "num_original_tables": len(original_tables),
        "num_processed_results": len(processed_results),
        "num_chains": len(chains),
        "is_multi_table": is_multi_table
    }
    save_debug_info(debug_qa_prompts_input)
    
    prompts = []
    for i, (orig_table, proc_result, chain) in enumerate(zip(original_tables, processed_results, chains)):
        proc_table = proc_result['final_table']
        if proc_table is None or len(proc_table) == 0:
            prompts.append(None)
            continue
            
        # 
        table_caption = table_captions[i] if table_captions and i < len(table_captions) else None
        foreign_key = foreign_keys[i] if foreign_keys and i < len(foreign_keys) else None
        
        # 
        # ：is_multi_table
        if is_multi_table:
            # 
            is_multi_structure = isinstance(orig_table, list) and len(orig_table) > 0 and isinstance(orig_table[0], list) and isinstance(orig_table[0][0], list)
            # 
            orig_table_str = generate_table_prompt(orig_table, is_multi_table=is_multi_table and is_multi_structure, table_names=table_caption, foreign_key=foreign_key)
        else:
            # 
            orig_table_str = generate_table_prompt(orig_table, is_multi_table=False)
        
        try:
            # 
            # ：is_multi_table
            if is_multi_table:
                # 
                is_multi_structure = isinstance(proc_table, list) and len(proc_table) > 0 and isinstance(proc_table[0], list) and isinstance(proc_table[0][0], list)
                # 
                proc_table_str = generate_table_prompt(proc_table, is_multi_table=is_multi_table and is_multi_structure, table_names=table_caption, foreign_key=foreign_key)
            else:
                # 
                proc_table_str = generate_table_prompt(proc_table, is_multi_table=False)
        except Exception as e:
            print(f": {str(e)}")
            prompts.append(None)
            continue
        
        qa_prompt = generate_qa_prompt(
            original_table=orig_table_str,
            chain_with_params=chain,
            final_table=proc_table_str,
            task_id=task_ID,
            random_seed=random.randint(1, 100),
            is_multi_table=is_multi_table
        )
        prompts.append(qa_prompt)
    
    # 
    debug_qa_prompts_output = {
        "type": "qa_prompts_output",
        "timestamp": str(import_module('datetime').datetime.now()),
        "num_prompts": len(prompts),
        "num_valid_prompts": sum(1 for p in prompts if p is not None),
        "sample_prompt": prompts[0][:200] if prompts and prompts[0] else None
    }
    save_debug_info(debug_qa_prompts_output)
    
    return prompts

def process_qa_responses(responses: List[str], processed_results: List[Dict[str, Any]], chains: List[List[str]], table_ids: List[str] = None) -> List[Dict[str, Any]]:
    """
    
    
    Args:
        responses: 
        processed_results: ，final_table、filled_chainsintermediate_tables
        chains: 
        table_ids: ID
        
    Returns:
        
    """
    results = []
    for i, (response, result, chain) in enumerate(zip(responses, processed_results, chains)):
        if response is None or result['final_table'] is None:
            continue
            
        try:
            question = response.split('Question:')[1].split('Answer:')[0].strip()
            answer = response.split('Answer:')[1].split('Explanation:')[0].strip()
            explanation = response.split('Explanation:')[1].strip()
            
            result_item = {
                'question': question,
                'answer': answer,
                'explanation': explanation,
                'table': result['final_table'],
                'chain': chain,
                'filled_chains': result['filled_chains'],
                'intermediate_tables': result['intermediate_tables']
            }
            
            # table_ids，id
            if table_ids is not None and i < len(table_ids) and table_ids[i] is not None:
                result_item['id'] = table_ids[i]
                
            results.append(result_item)
        except Exception as e:
            logger.error(f": {str(e)}")
            continue
    
    return results

def generate_qa_pairs_batch(tables: List[List[List[Any]]], chains: List[List[str]], llm: LLM, sampling_params: SamplingParams, table_ids: List[str] = None, is_multi_table: bool = False, table_captions: List[str] = None, foreign_keys: List[str] = None) -> List[Dict[str, Any]]:
    """
    
    
    Args:
        tables: 
        chains: 
        llm: 
        sampling_params: 
        table_ids: ID
        is_multi_table: 
        table_captions: 
        foreign_keys: 
        
    Returns:
        
    """
    # 
    processed_tables = []
    table_captions_list = []
    foreign_keys_list = []
    
    for i, table in enumerate(tables):
        if is_multi_table and isinstance(table, dict):
            # 
            processed_tables.append(table["table"])
            table_captions_list.append(table.get("table_caption"))
            foreign_keys_list.append(table.get("foreign_key"))
        else:
            # 
            processed_tables.append(table)
            if table_captions and i < len(table_captions):
                table_captions_list.append(table_captions[i])
            else:
                table_captions_list.append(None)
            if foreign_keys and i < len(foreign_keys):
                foreign_keys_list.append(foreign_keys[i])
            else:
                foreign_keys_list.append(None)
    
    # 1. 
    chain_params = generate_chain_params_batch(processed_tables, chains, llm, sampling_params, is_multi_table, table_captions_list, foreign_keys_list)
    
    # 2. 
    processed_results = process_tables_with_params(processed_tables, chains, chain_params, llm, sampling_params, is_multi_table, table_captions_list, foreign_keys_list)
    
    # 3. 
    qa_prompts = generate_qa_prompts_batch(original_tables=processed_tables, processed_results=processed_results, chains=chains, is_multi_table=is_multi_table, table_captions=table_captions_list, foreign_keys=foreign_keys_list)
    
    # 4. 
    valid_prompts = [p for p in qa_prompts if p is not None]
    if not valid_prompts:
        return []
    
    sampling_params = SamplingParams(temperature=0, top_p=0.95, max_tokens=512)
    qa_responses = chat(llm, sampling_params, valid_prompts, "")
    
    # 5. 
    valid_indices = [i for i, p in enumerate(qa_prompts) if p is not None]
    valid_processed_results = [processed_results[i] for i in valid_indices]
    valid_chains = [chains[i] for i in valid_indices]
    
    # ID
    valid_table_ids = None
    if table_ids is not None:
        valid_table_ids = [table_ids[i] for i in valid_indices]
    
    results = process_qa_responses(qa_responses, valid_processed_results, valid_chains, valid_table_ids)
    
    return results

def main():
    # 
    parser = argparse.ArgumentParser()
    parser.add_argument("--train_file_root", type=str)
    parser.add_argument("--processed_file_root", type=str)
    parser.add_argument("--output_file_root", type=str)
    parser.add_argument("--model_path", type=str)
    args = parser.parse_args()
    train_file_root = args.train_file_root
    processed_file_root = args.processed_file_root
    output_file_root = args.output_file_root
    model_path = args.model_path
    is_multi_table = [True, False, False, True, False, True, False, True, True]
    every_task_num = 500
    # is_multi_table
    print("mainis_multi_table:", is_multi_table)
    
    # 
    llm = LLM(model=model_path, tensor_parallel_size=2, gpu_memory_utilization=0.95, max_model_len=12000)
    print("Loading...")    
    os.system("nvidia-smi")
    sampling_params = SamplingParams(temperature=0, top_p=0.95, max_tokens=2048)
    for task_id in range(4, 9):
        global task_ID
        task_ID = task_id
        global task_ID_debug_path
        task_ID_debug_path = f"{task_ID_debug_path_root}/task_{task_id}.json"
        # taskmulti_table
        task_multi_table = is_multi_table[task_id]
        
        # QA
        outputs = []
        
        # task
        train_file = f"{train_file_root}/task_{task_id}/train.json"
        train_multi_file = f"{train_file_root}/task_{task_id}/train_multi.json"
        output_file = f"{output_file_root}/generated_qa_pairs_{task_id}_gaps.json"
        
        # chain-table
        used_pairs = set()
        
        # former_id，0，500QA
        former_id_list = list(range(task_id))
        former_id_idx = 0
        
        # former_id_list
        if not former_id_list:
            print(f"task_{task_id}former_id，")
            continue
        
        while len(outputs) < every_task_num and former_id_list:
            # former_id，
            former_id = former_id_list[former_id_idx % len(former_id_list)]
            former_id_idx += 1
            
            # former_idmulti_table
            former_multi_table = is_multi_table[former_id]
            print(f"task_{task_id}former_id={former_id}，former_multi_table={former_multi_table}, task_multi_table={task_multi_table}")
            
            # gaps
            gaps_file = os.path.join(processed_file_root, f"processed_chains_{former_id}_for_{task_id}_gaps.json")
            
            # 
            if not os.path.exists(gaps_file):
                print(f"{gaps_file}，")
                continue
                
            try:
                with open(gaps_file, 'r', encoding='utf-8') as fp:
                    gaps_data = json.load(fp)
            except Exception as e:
                print(f"{gaps_file}: {str(e)}，")
                continue
            
            # gaps chains
            chains = []
            for item in gaps_data:
                if "chain" in item.keys():
                    chains.append(item["chain"])
            chains = [list(x) for x in set(tuple(chain) for chain in chains)]
            
            if not chains:
                print(f"former_id={former_id}gaps chains，")
                continue
                
            # 
            if former_multi_table == task_multi_table:
                # task
                print(f"former_multi_tabletask_multi_table，train.json")
                tables = convert_to_ftct_format(train_file, former_multi_table)
            elif former_multi_table and not task_multi_table:
                # former，task，train_multi.json
                print(f"former_multi_table=True，task_multi_table=False，train_multi.json")
                if os.path.exists(train_multi_file):
                    tables = convert_to_ftct_format(train_multi_file, former_multi_table)
                else:
                    print(f"train_multi.json，")
                    continue
            else:
                # former，task，
                print(f"former_multi_table=False，task_multi_table=True，")
                multi_tables = convert_to_ftct_format(train_file, True)
                tables = []
                for item in multi_tables:
                    # 
                    if "table_info" in item and "table_text" in item["table_info"] and len(item["table_info"]["table_text"]) > 0:
                        single_item = {
                            "id": item["id"],
                            "table_info": {
                                "table_text": item["table_info"]["table_text"][0] if isinstance(item["table_info"]["table_text"][0], list) else item["table_info"]["table_text"]
                            }
                        }
                        tables.append(single_item)
            
            # 
            train_data = []
            for item in tables:
                if former_multi_table:
                    # 
                    train_item = {
                        "id": item["id"],  # ID
                        "table": item["table_info"]["table_text"],
                        "table_caption": item["table_caption"] if "table_caption" in item else None,
                        "foreign_key": item["table_info"]["foreign_key"] if "foreign_key" in item["table_info"] else None
                    }
                else:
                    # 
                    train_item = {
                        "id": item["id"],  # ID
                        "table": item["table_info"]["table_text"]
                    }
                train_data.append(train_item)
            
            if not train_data:
                print(f"，")
                continue
                
            # former_idchains
            sub_batch_size = 32  # GPU
            
            # chain
            chain_iterator = itertools.cycle(chains)
            
            # 
            while len(outputs) < every_task_num:
                # chain
                sub_batch_tables = []
                sub_batch_chains = []
                sub_batch_ids = []  # ID
                sub_batch_table_captions = []  # 
                sub_batch_foreign_keys = []  # 
                
                # 
                attempts = 0
                max_attempts = 1000  # ，
                
                while len(sub_batch_tables) < sub_batch_size and attempts < max_attempts:
                    with open("help.txt", "a", encoding="utf-8") as f:
                        f.write(f": {len(sub_batch_tables)}，: {attempts}\n")
                    # 
                    random_item = random.choice(train_data)
                    random_table = random_item['table']
                    table_id = random_item['id']  # ID
                    
                    # （）
                    table_caption = random_item.get('table_caption')
                    foreign_key = random_item.get('foreign_key')
                    
                    # chain
                    current_chain = next(chain_iterator)
                    
                    # 
                    if isinstance(random_table[0], list) and isinstance(random_table[0][0], list):
                        # ，
                        # ，
                        table_tuple = tuple(tuple(tuple(row) if isinstance(row, list) else row for row in table) 
                                         if isinstance(table, list) else table for table in random_table)
                        caption_tuple = tuple(table_caption) if table_caption and isinstance(table_caption, list) else table_caption
                        # 
                        if isinstance(foreign_key, list):
                            foreign_key_tuple = tuple(tuple(fk) if isinstance(fk, list) else fk for fk in foreign_key)
                        else:
                            foreign_key_tuple = foreign_key
                        
                        pair_id = (tuple(current_chain), table_tuple, caption_tuple, foreign_key_tuple)
                    else:
                        # 
                        # ，
                        table_tuple = tuple(tuple(row) for row in random_table)
                        pair_id = (tuple(current_chain), table_tuple)
                    
                    # 
                    if pair_id not in used_pairs:
                        sub_batch_tables.append(random_table)
                        sub_batch_chains.append(current_chain)
                        sub_batch_ids.append(table_id)  # ID
                        sub_batch_table_captions.append(table_caption)
                        sub_batch_foreign_keys.append(foreign_key)
                        used_pairs.add(pair_id)
                    else:
                        with open("help.txt", "a", encoding="utf-8") as f:
                            f.write(f"，, ：{str(used_pairs)}\n")
                    
                    attempts += 1
                
                # ，
                if not sub_batch_tables:
                    with open("help.txt", "a", encoding="utf-8") as f:
                        f.write(f"：former_id={former_id}chain-table，former_id\n")
                    break
                
                # 
                with open("help.txt", "a", encoding="utf-8") as f:
                    f.write(f"former_id={former_id}chains: multi_table_identifier={former_multi_table}\n")
                batch_results = generate_qa_pairs_batch(
                    tables=sub_batch_tables,
                    chains=sub_batch_chains,
                    llm=llm,
                    sampling_params=sampling_params,
                    table_ids=sub_batch_ids,  # ID
                    is_multi_table=former_multi_table,  # former_idmulti_table
                    table_captions=sub_batch_table_captions,
                    foreign_keys=sub_batch_foreign_keys
                )
                outputs.extend(batch_results)
                
                # GPU
                torch.cuda.empty_cache()
                
                # 
                with open("help.txt", "a", encoding="utf-8") as f:
                    f.write(f" {len(outputs)} ，former_id={former_id}{len(batch_results)}， {len(used_pairs)} \n")
                
                break
                # 500，
                if len(outputs) >= every_task_num:
                    break
            
            # 500，
            if len(outputs) >= every_task_num:
                with open("help.txt", "a", encoding="utf-8") as f:
                    f.write(f"{len(outputs)}QA，，\n")
                break
            
        # 
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(outputs, f, ensure_ascii=False, indent=2)
        
        with open("help.txt", "a", encoding="utf-8") as f:
            f.write(f" {len(outputs)} ， {len(used_pairs)} \n")

if __name__ == "__main__":
    main()
