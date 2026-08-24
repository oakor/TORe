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

# 
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

task_ID = 0

def generate_table_prompt(table_text: List[List[str]]) -> str: 
    """
    
    """
    prompt = ""
    prompt += "/*\n"
    prompt += "col : " + " | ".join([str(item) for item in table_text[0]]) + " |\n"
    for idx, row in enumerate(table_text[1:], 1):
        prompt += "row " + str(idx) + " : " + " | ".join([str(item) for item in row]) + " |\n"
    prompt += "*/\n"
    return prompt

def chat(llm, sampling_params, prompts, system_prompt):
    """
    
    
    Args:
        llm: 
        sampling_params: 
        prompts: 
        system_prompt: 
        
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
    outputs = llm.chat(messages,
                    sampling_params=sampling_params,
                    use_tqdm=True)
    print(outputs)
    
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
    
    return generated_texts

def process_table_with_chain(table: List[List[Any]], chain: List[str], llm, sampling_params) -> List[List[Any]]:
    """
    
    
    Args:
        table: 
        chain: 
        llm: 
        sampling_params: 
        
    Returns:
        
    """
    current_table = table.copy()
    table_str = generate_table_prompt(current_table)
    
    # 
    chain_param_prompt = generate_chain_param_prompt(
        table_info=table_str,
        chain=chain,
        task_id=task_ID,
        random_seed=random.randint(1, 100)
    )
    chain_param_response = chat(llm, sampling_params, [chain_param_prompt], "")[0]
    
    print("chain_param_prompt: ", chain_param_prompt)
    print("chain_param_response: ", chain_param_response)
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
                print("--------------------------------")
                print("op: ", op)
                print("values_prompt: ", values_prompt)
                print("values: ", values)
                print("current_table: ", current_table)
                print("--------------------------------")
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
                print("--------------------------------")
                print("op: ", op)
                print("values_prompt: ", values_prompt)
                print("values: ", values)
                print("current_table: ", current_table)
                print("--------------------------------")
            elif op.startswith('f_sort_column'):
                col_name = op.split('(')[1].split(')')[0].strip()
                orders = ["small to large", "large to small"]
                order = random.choice(orders)
                current_table = process_sort_column(current_table, col_name, order)
                print("--------------------------------")
                print("op: ", op)
                print("current_table: ", current_table)
                print("--------------------------------")
            elif op.startswith('f_select_column'):
                cols = op.split('(')[1].split(')')[0].strip().split(',')
                cols = [col.strip() for col in cols]
                current_table = process_select_column(current_table, cols)
                print("--------------------------------")
                print("op: ", op)
                print("current_table: ", current_table)
                print("--------------------------------")
            elif op.startswith('f_select_row'):
                rows = op.split('(')[1].split(')')[0].strip().split(',')
                print("rows: ", rows)
                rows = [int(row.strip().split(' ')[-1]) for row in rows]
                current_table = process_select_row(current_table, rows)
                print("--------------------------------")
                print("op: ", op)
                print("current_table: ", current_table)
                print("--------------------------------")
            elif op.startswith('f_group_column'):
                col_name = op.split('(')[1].split(')')[0].strip().split(',')
                current_table = process_group_column(current_table, col_name)
                print("--------------------------------")
                print("op: ", op)
                print("current_table: ", current_table)
                print("--------------------------------")
            elif op.startswith('f_stitch_tables'):
                # 
                pass
                
            elif op.startswith('f_change_column_name'):
                old_name, new_name = op.split('(')[1].split(')')[0].strip().split(',')
                old_name = old_name.strip().strip('"')
                new_name = new_name.strip().strip('"')
                current_table = process_change_column_name(current_table, old_name, new_name)
                print("--------------------------------")
                print("op: ", op)
                print("current_table: ", current_table)
                print("--------------------------------")
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

def generate_chain_params_batch(tables: List[List[List[Any]]], chains: List[List[str]], llm: LLM, sampling_params: SamplingParams) -> List[Dict[str, Any]]:
    """
    
    
    Args:
        tables: 
        chains: 
        llm: 
        sampling_params: 
        
    Returns:
        
    """
    # 
    prompts = []
    for table, chain in zip(tables, chains):
        table_str = generate_table_prompt(table)
        chain_param_prompt = generate_chain_param_prompt(
            table_info=table_str,
            chain=chain,
            task_id=task_ID,
            random_seed=random.randint(1, 100)
        )
        prompts.append(chain_param_prompt)
    
    # 
    responses = chat(llm, sampling_params, prompts, "")
    
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
    
    return results

def process_tables_with_params(tables: List[List[List[Any]]], chains: List[List[str]], params_list: List[Dict[str, Any]], llm: LLM, sampling_params: SamplingParams) -> List[List[List[Any]]]:
    """
    
    
    Args:
        tables: 
        chains: 
        params_list: 
        llm: 
        sampling_params: 
        
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
    processed_tables = []
    current_tables = [table.copy() for table in tables]
    
    # 
    op_indices = [0] * len(tables)
    
    # 
    completed = [False] * len(tables)
    
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
                table_str = generate_table_prompt(current_tables[table_idx])
            except Exception as e:
                logger.error(f" {table_idx} : {str(e)}")
                completed[table_idx] = True
                continue
            
            try:
                # 
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
                    
                elif op.startswith('f_stitch_tables'):
                    # 
                    pass
                    
                elif op.startswith('f_change_column_name'):
                    old_name, new_name = op.split('(')[1].split(')')[0].strip().split(',')
                    old_name = old_name.strip().strip('"')
                    new_name = new_name.strip().strip('"')
                    current_tables[table_idx] = process_change_column_name(current_tables[table_idx], old_name, new_name)
                    print("--------------------------------")
                    print("op: ", op)
                    print("current_table: ", current_tables[table_idx])
                    print("--------------------------------")
                
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
    for table in current_tables:
        processed_tables.append(table)
    
    return processed_tables

def generate_qa_prompts_batch(original_tables: List[List[List[Any]]], 
                            processed_tables: List[List[List[Any]]], 
                            chains: List[List[str]]) -> List[str]:
    """
    
    
    Args:
        original_tables: 
        processed_tables: 
        chains: 
        
    Returns:
        
    """
    prompts = []
    for orig_table, proc_table, chain in zip(original_tables, processed_tables, chains):
        if proc_table is None or len(proc_table) == 0:
            prompts.append(None)
            continue
            
        orig_table_str = generate_table_prompt(orig_table)
        try:
            proc_table_str = generate_table_prompt(proc_table)
        except Exception as e:
            print(f": {str(e)}")
            prompts.append(None)
            continue
        
        qa_prompt = generate_qa_prompt(
            original_table=orig_table_str,
            chain_with_params=chain,
            final_table=proc_table_str,
            task_id=task_ID,
            random_seed=random.randint(1, 100)
        )
        prompts.append(qa_prompt)
    
    return prompts

def process_qa_responses(responses: List[str], processed_tables: List[List[List[Any]]], chains: List[List[str]], table_ids: List[str] = None) -> List[Dict[str, Any]]:
    """
    
    
    Args:
        responses: 
        processed_tables: 
        chains: 
        table_ids: ID
        
    Returns:
        
    """
    results = []
    for i, (response, table, chain) in enumerate(zip(responses, processed_tables, chains)):
        if response is None or table is None:
            continue
            
        try:
            question = response.split('Question:')[1].split('Answer:')[0].strip()
            answer = response.split('Answer:')[1].split('Explanation:')[0].strip()
            explanation = response.split('Explanation:')[1].strip()
            
            result_item = {
                'question': question,
                'answer': answer,
                'explanation': explanation,
                'table': table,
                'chain': chain
            }
            
            # table_ids，id
            if table_ids is not None and i < len(table_ids) and table_ids[i] is not None:
                result_item['id'] = table_ids[i]
                
            results.append(result_item)
        except Exception as e:
            logger.error(f": {str(e)}")
            continue
    
    return results

def generate_qa_pairs_batch(tables: List[List[List[Any]]], chains: List[List[str]], llm: LLM, sampling_params: SamplingParams, table_ids: List[str] = None) -> List[Dict[str, Any]]:
    """
    
    
    Args:
        tables: 
        chains: 
        llm: 
        sampling_params: 
        table_ids: ID
        
    Returns:
        
    """
    # 1. 
    chain_params = generate_chain_params_batch(tables, chains, llm, sampling_params)
    
    # 2. 
    processed_tables = process_tables_with_params(tables, chains, chain_params, llm, sampling_params)
    
    # 3. 
    qa_prompts = generate_qa_prompts_batch(tables, processed_tables, chains)
    
    # 4. 
    valid_prompts = [p for p in qa_prompts if p is not None]
    if not valid_prompts:
        return []
        
    qa_responses = chat(llm, sampling_params, valid_prompts, "")
    
    # 5. 
    valid_indices = [i for i, p in enumerate(qa_prompts) if p is not None]
    valid_processed_tables = [processed_tables[i] for i in valid_indices]
    valid_chains = [chains[i] for i in valid_indices]
    
    # ID
    valid_table_ids = None
    if table_ids is not None:
        valid_table_ids = [table_ids[i] for i in valid_indices]
    
    results = process_qa_responses(qa_responses, valid_processed_tables, valid_chains, valid_table_ids)
    
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
    # 
    llm = LLM(model=model_path, tensor_parallel_size=2, max_model_len=6000)
    print("Loading...")    
    os.system("nvidia-smi")
    sampling_params = SamplingParams(temperature=0, top_p=0.95, max_tokens=2048)
    for task_id in range(8, 9):
        global task_ID
        task_ID = task_id
        train_file = f"{train_file_root}/task_{task_id}/train.json"
        processed_file = f"{processed_file_root}/processed_chains_{task_id}_gaps.json"
        output_file = f"{output_file_root}/generated_qa_pairs_{task_id}_gaps.json"
        
    
        
        # 
        tables = convert_to_ftct_format(train_file)
        train_data = []
        for item in tables:
            train_data.append({
                "id": item["id"],  # ID
                "table": item["table_info"]["table_text"]
            })
        
        # 
        try:
            with open(processed_file, 'r', encoding='utf-8') as fp:
                processed_data = json.load(fp)
        except UnicodeDecodeError:
            #  utf-8 ，
            with open(processed_file, 'r', encoding='latin-1') as fp:
                processed_data = json.load(fp)
        
        # 
        chains = []
        for item in processed_data:
            if "chain" in item.keys():
                chains.append(item["chain"])
        chains = [list(x) for x in set(tuple(chain) for chain in chains)]
        
        # 
        outputs = []

        sub_batch_size = 32  # GPU
        
        # chain
        chain_iterator = itertools.cycle(chains)
        
        # chain-table
        used_pairs = set()
        
        # 
        while len(outputs) < 500:
            # chain
            sub_batch_tables = []
            sub_batch_chains = []
            sub_batch_ids = []  # ID
            
            # 
            attempts = 0
            max_attempts = 1000  # ，
            
            while len(sub_batch_tables) < sub_batch_size and attempts < max_attempts:
                # 
                random_item = random.choice(train_data)
                random_table = random_item['table']
                table_id = random_item['id']  # ID
                
                # chain
                current_chain = next(chain_iterator)
                
                # 
                pair_id = (tuple(current_chain), tuple(map(tuple, random_table)))
                
                # 
                if pair_id not in used_pairs:
                    sub_batch_tables.append(random_table)
                    sub_batch_chains.append(current_chain)
                    sub_batch_ids.append(table_id)  # ID
                    used_pairs.add(pair_id)
                
                attempts += 1
            
            # ，
            if not sub_batch_tables:
                print("：chain-table")
                break
            
            # 
            batch_results = generate_qa_pairs_batch(
                tables=sub_batch_tables,
                chains=sub_batch_chains,
                llm=llm,
                sampling_params=sampling_params,
                table_ids=sub_batch_ids  # ID
            )
            outputs.extend(batch_results)
            
            # GPU
            torch.cuda.empty_cache()
            
            # 
            print(f" {len(outputs)} ， {len(used_pairs)} ")
        
        # 
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(outputs, f, ensure_ascii=False, indent=2)
        
        print(f" {len(outputs)} ， {len(used_pairs)} ")

if __name__ == "__main__":
    main()
