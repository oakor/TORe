import os
import json
import re
import logging
from typing import List, Dict, Tuple, Any, Optional, Union
import vllm
from vllm import LLM, SamplingParams
import torch

from demos import *
from operations.add_columns import extract_add_column_params, process_add_column
from operations.add_knowledge_column import extract_add_knowledge_column_params, process_add_knowledge_column
from operations.add_inferred_column import extract_add_inferred_column_params, process_add_inferred_column
from operations.select_column import extract_select_column_params, process_select_column
from operations.sort_column import extract_sort_column_params, process_sort_column
from operations.select_row import extract_select_row_params, process_select_row
from operations.group_column import extract_group_column_params, process_group_column
from operations.change_column_name import extract_change_column_name_params, process_change_column_name
from operations.stitch_tables import extract_stitch_tables_params, process_stitch_tables

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class Ftct:
    """
    Fast Table Chain of Thought (Ftct) for table question answering.
    This class implements a simplified version of table question answering system.
    """
    
    def __init__(self, model_path: str, max_chain_length: int = 5, debug: bool = False):
        self.max_chain_length = max_chain_length
        self.debug = debug
        if self.debug:
            self.responses_log = []
        self.llm = LLM(
            model=model_path,
            trust_remote_code=True,
            tensor_parallel_size=2,
            gpu_memory_utilization=0.9,
            max_num_batched_tokens=8192, 
        )
        
        self.operations = [
            "f_add_knowledge_column",
            "f_add_inferred_column",
            "f_sort_column",
            "f_select_column",
            "f_select_row",
            "f_group_column",
            "f_change_column_name",
            "END"
        ]
        
        # 
        self.load_examples()
        
        # 
        self.select_sampling_params = SamplingParams(
            temperature=0.7,
            top_p=0.9,
            max_tokens=1024
        )
        
        self.operation_sampling_params = SamplingParams(
            temperature=0.7,
            top_p=0.9,
            max_tokens=1024,
            n=5  # 5
        )
    
    def __del__(self):
        """"""
        torch.cuda.empty_cache()
    
    def load_examples(self):
        """"""
        self.examples = select_demos
        self.examples.pop("f_stitch_tables", None)
        self.operation_examples = {
            "f_add_knowledge_column": f_add_knowledge_column_demos,
            "f_add_inferred_column": f_add_inferred_column_demos,
            "f_sort_column": f_sort_column_demos,
            "f_select_column": f_select_column_demos,
            "f_select_row": f_select_row_demos,
            "f_group_column": f_group_column_demos,
            "f_change_column_name": f_change_column_name_demos,
            "f_stitch_tables": f_stitch_tables_demos
        }
    
    def _build_multi_table_prompt_content(self, tables, captions, foreign_keys):
        prompt_content = "/*"
        for i, single_table in enumerate(tables):
            table_md = f"table_name: {captions[i]}\n"
            table_md += "col : " + " | ".join([str(item) for item in single_table[0]]) + " |\n"
            for idx, row in enumerate(single_table[1:], 1):
                table_md += "row " + str(idx) + " : " + " | ".join([str(item) for item in row]) + " |\n"
            prompt_content += "\n" + table_md
        if foreign_keys:
            prompt_content += f"\nforeign_key: {', '.join(foreign_keys)}\n"
        prompt_content += "*/\n"
        return prompt_content

    def generate_prompt(self, table_text: List[List[str]], question: str, 
                       table_caption: Optional[str] = None, 
                       chain_so_far: Optional[List[str]] = None,
                       multi_table: bool = False,
                       foreign_keys: Optional[List[str]] = None) -> str:
        """
        
        
        Args:
            table_text: 
            question: 
            table_caption: 
            chain_so_far: 
            multi_table: 
            foreign_keys: 
            
        Returns:
            
        """
        # markdown
        table_md = ""
        for idx, row in enumerate(table_text[1:], 1):
            table_md += "row " + str(idx) + " : " + " | ".join([str(item) for item in row]) + " |\n"
        
        # 
        prompt = "# Instruction\n"
        prompt += "You are a table processing assistant. Your task is to select the correct operation to process the given table step by step to answer the question.\n\n"
        
        # 
        prompt += "## Output Format\n"
        prompt += "You MUST follow this exact format:\n\n"
        prompt += "1. For Operation (except END):\n"
        prompt += "Explanation: [explanation]\n"
        prompt += "Function: [function]\n"
        prompt += "\n\n"
        
        prompt += "2. For END:\n"
        prompt += "Explanation: [explanation]\n"
        prompt += "Function: END\n"
        prompt += "Answer: [your final answer]\n"
        prompt += "\n\n"

        prompt += "## Rules\n"
        prompt += "1. You MUST choose exactly one operation from the available operations\n"
        prompt += "2. You MUST follow the exact output format\n"
        prompt += "3. For table operations, you MUST include the complete new table\n"
        prompt += "4. For END operation, you MUST provide a clear and concise answer\n"
        prompt += "5. Do not include any explanations or additional text\n"

        # 
        prompt += "## Available Operations\n"
        for op in self.operations:
            if op in chain_so_far or "skip " + op in chain_so_far:
                continue
            prompt += f"- {op}\n"
        prompt += "\n"

        # 
        prompt += "## Examples\n"
        for op, example in self.examples.items():
            if op in chain_so_far or "skip " + op in chain_so_far:
                continue
            prompt += f"{example}\n"
        
        # 
        prompt += "## Current Table\n"
        if multi_table and isinstance(table_text[0][0], list):
            prompt += self._build_multi_table_prompt_content(table_text, table_caption, foreign_keys)
        else:
            if table_caption:
                prompt += f"Table caption: {table_caption}\n"
            table_md = "col : " + " | ".join([str(item) for item in table_text[0]]) + " |\n"
            for idx, row in enumerate(table_text[1:], 1):
                table_md += "row " + str(idx) + " : " + " | ".join([str(item) for item in row]) + " |\n"
            prompt += "/*\n" + table_md + "\n*/\n"
        
        # 
        prompt += "Question: "
        prompt += f"{question}\n"

        prompt += "Explanation:"
        
        return prompt

    def generate_operation_prompt(self, operation: str, table_text: List[List[str]], question: str) -> str: 
        """
        
        """
        prompt = self.operation_examples[operation]
        prompt += "/*\n"
        prompt += "col : " + " | ".join([str(item) for item in table_text[0]]) + " |\n"
        for idx, row in enumerate(table_text[1:], 1):
            prompt += "row " + str(idx) + " : " + " | ".join([str(item) for item in row]) + " |\n"
        prompt += "*/\n"
        prompt += "Question: " + question + "\n"
        return prompt
    
    def process_operation(self, operation: str, llm_output: str, current_table: List[List[str]], table_caption: Optional[List[str]] = None) -> Optional[List[List[str]]]:
        """"""
        try:
            if operation == "f_add_knowledge_column":
                columns, values = extract_add_knowledge_column_params(llm_output)
                if columns:
                    new_table = process_add_knowledge_column(current_table, columns, values)
                    if new_table and new_table[0]:
                        return new_table
            elif operation == "f_add_inferred_column":
                columns, values = extract_add_inferred_column_params(llm_output)
                if columns:
                    new_table = process_add_inferred_column(current_table, columns, values)
                    if new_table and new_table[0]:
                        return new_table
            elif operation == "f_select_column":
                columns = extract_select_column_params(llm_output)
                if columns:
                    new_table = process_select_column(current_table, columns)
                    if new_table and new_table[0]:
                        return new_table
            elif operation == "f_sort_column":
                column, order = extract_sort_column_params(llm_output)
                if column:
                    new_table = process_sort_column(current_table, column, order)
                    if new_table and new_table[0]:
                        return new_table
            elif operation == "f_select_row":
                rows = extract_select_row_params(llm_output)
                if rows:
                    new_table = process_select_row(current_table, rows)
                    if new_table and new_table[0]:
                        return new_table
            elif operation == "f_group_column":
                column = extract_group_column_params(llm_output)
                if column:
                    new_table = process_group_column(current_table, column)
                    if new_table and new_table[0]:
                        return new_table
            elif operation == "f_change_column_name":
                columns, values = extract_change_column_name_params(llm_output)
                if columns:
                    new_table = process_change_column_name(current_table, columns, values)
                    if new_table and new_table[0]:
                        return new_table
            elif operation == "f_stitch_tables":
                params = extract_stitch_tables_params(llm_output)
                if params:
                    new_table = process_stitch_tables(current_table, table_caption, params)
                    if new_table and new_table[0]:
                        return new_table
        except Exception as e:
            logger.error(f": {str(e)}")
        return None

    def process_batch(self, batch: List[Dict[str, Any]], max_operations: int) -> List[Dict[str, Any]]:
        # 1. Initialization
        for s in batch:
            s["chain"] = s.get("chain", [])
            table_text = s.get("table_info", {}).get("table_text", [])
            s["is_multi_table"] = bool(table_text and isinstance(table_text[0], list) and table_text[0] and isinstance(table_text[0][0], list))
            s["status"] = "active" # status: active, finished

        # 2. Multi-table pre-processing in a batch
        multi_table_samples = [s for s in batch if s["is_multi_table"]]
        if multi_table_samples:
            prompts = []
            for sample in multi_table_samples:
                multi_table_prompt_content = self._build_multi_table_prompt_content(
                    sample["table_info"]["table_text"], sample.get("table_caption"), sample.get("table_info", {}).get("foreign_key")
                )
                prompt_content = multi_table_prompt_content + f"\nQuestion: {sample.get('statement', '')}\nExplanation:"
                prompts.append(stitch_decision_prompt_template.format(prompt_content=prompt_content))

            outputs = self.llm.generate(prompts, self.select_sampling_params)

            for i, sample in enumerate(multi_table_samples):
                llm_output = outputs[i].outputs[0].text
                if self.debug:
                    self.responses_log.append({"id": sample.get("id"), "type": "stitch_decision", "prompt": prompts[i], "response": llm_output})

                stitch_match = re.search(r"Function:\s*f_stitch_tables\(.*\)", llm_output)
                select_match = re.search(r"Function:\s*f_select_table\((.+)\)", llm_output)

                if stitch_match:
                    new_table = self.process_operation("f_stitch_tables", llm_output, sample["table_info"]["table_text"], sample.get("table_caption"))
                    if new_table:
                        sample["chain"].append("f_stitch_tables")
                        sample["table_info"]["table_text"] = new_table
                        sample["is_multi_table"] = False
                        sample["table_caption"] = None
                    else:
                        sample["chain"].append("skip f_stitch_tables")
                elif select_match:
                    table_to_keep = select_match.group(1).strip()
                    try:
                        table_idx = sample.get("table_caption").index(table_to_keep)
                        sample["table_info"]["table_text"] = sample["table_info"]["table_text"][table_idx]
                        sample["table_caption"] = table_to_keep
                        sample["is_multi_table"] = False
                        sample["chain"].append(f"select_table({table_to_keep})")
                    except (ValueError, IndexError):
                        sample["chain"].append(f"skip select_table({table_to_keep})")
                else:
                    sample["chain"].append("skip stitch_decision")
        torch.cuda.empty_cache()
        # 3. Main iterative processing loop
        for _ in range(max_operations):
            active_samples = [s for s in batch if s["status"] == "active" and len(s["chain"]) < max_operations]
            if not active_samples:
                break

            # 3.1. Generate select_operation prompts
            prompts = [self.generate_prompt(
                s["table_info"]["table_text"], s["statement"], s.get("table_caption"), s["chain"]
            ) for s in active_samples]
            select_op_outputs = self.llm.generate(prompts, self.select_sampling_params)

            # 3.2. Parse operations and prepare for parameter generation
            param_gen_samples = []
            for i, sample in enumerate(active_samples):
                output_text = select_op_outputs[i].outputs[0].text
                op_match = re.search(r"Function:\s*(\w+)", output_text)
                operation = op_match.group(1) if op_match else "skip"
                
                if operation == "END":
                    sample["status"] = "finished"
                    answer_match = re.search(r"Answer:\s*(.+)", output_text)
                    sample["answer"] = answer_match.group(1).strip() if answer_match else ""
                elif operation != "skip" and operation in self.operation_examples:
                    sample["current_operation"] = operation
                    param_gen_samples.append(sample)
                else:
                    sample["chain"].append(f"skip invalid_operation({operation})")
            torch.cuda.empty_cache()
            if not param_gen_samples:
                continue

            # 3.3. Generate parameters
            param_prompts = [self.generate_operation_prompt(
                s['current_operation'], s["table_info"]["table_text"], s["statement"]
            ) for s in param_gen_samples]
            
            # param_prompts4，
            # param_outputs = []
            # batch_size = max(1, len(param_prompts) // 4)  # 1
            
            # for i in range(0, len(param_prompts), batch_size):
            #     batch_prompts = param_prompts[i:i+batch_size]
            #     batch_outputs = self.llm.generate(batch_prompts, self.operation_sampling_params)
            #     param_outputs.extend(batch_outputs)
            #     torch.cuda.empty_cache()

            param_outputs = self.llm.generate(param_prompts, self.operation_sampling_params)
            torch.cuda.empty_cache()

            # 3.4. Process operations with parameters
            for i, sample in enumerate(param_gen_samples):
                operation = sample['current_operation']
                llm_choices = [out.text for out in param_outputs[i].outputs]
                new_table = None
                for choice in llm_choices:
                    result = self.process_operation(operation, choice, sample["table_info"]["table_text"])
                    if result is not None:
                        new_table = result
                        break
                
                if new_table is not None:
                    sample["chain"].append(operation)
                    sample["table_info"]["table_text"] = new_table
                else:
                    sample["chain"].append(f"skip {operation}")
        
        # 4. Final cleanup
        for sample in batch:
            sample.pop("is_multi_table", None)
            sample.pop("status", None)
            sample.pop("current_operation", None)
            if "answer" not in sample:
                sample["answer"] = "Reached max operations."
        
        return batch

    def save_responses_log(self, output_file: str = "running_response.json"):
        """promptresponse"""
        if self.debug and self.responses_log:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(self.responses_log, f, ensure_ascii=False, indent=4)
            logger.info(f" {output_file}") 