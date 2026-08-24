import os
import json
import argparse
from ftct import Ftct
from tqdm import tqdm
from utils import convert_to_ftct_format, save_ftct_format
from typing import List, Dict, Any
import torch

def process_batch(ftct: Ftct, batch: List[Dict[str, Any]], max_operations: int) -> List[Dict[str, Any]]:
    """"""
    results = ftct.process_batch(batch, max_operations)
    # GPU
    torch.cuda.empty_cache()
    return results

def main():
    parser = argparse.ArgumentParser(description='Fast Table Chain of Thought')
    parser.add_argument('--model_path', type=str, required=True, help='Path to the model')
    parser.add_argument('--input_file', type=str, required=True, help='Path to the input file')
    parser.add_argument('--output_file', type=str, required=True, help='Path to the output file')
    parser.add_argument('--max_operations', type=int, default=7, help='Maximum number of operations')
    parser.add_argument('--batch_size', type=int, default=4, help='Batch size for processing')
    parser.add_argument('--multi_table', type=bool, default=False, help='Whether to process multi-table data')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode to save prompts and responses')
    args = parser.parse_args()
    print("args.multi_table", args.multi_table)
    #  Ftct
    ftct = Ftct(args.model_path, debug=args.debug)
    task_ids = [0,1,2,3,4,5,6,7,8]
    for task_id in task_ids:
        input_path = os.path.join(args.input_file, f"task_{task_id}", "train.json")
        output_path = os.path.join(args.output_file, f"task_{task_id}")
        if not os.path.exists(output_path):
            os.mkdir(output_path)
        output_path = os.path.join(output_path, "train.json")
        
        # 
        print("Converting input data...")
        ftct_data = convert_to_ftct_format(input_path, args.multi_table)
        
        # 
        batches = [ftct_data[i:i + args.batch_size] for i in range(0, len(ftct_data), args.batch_size)]
        
        # 
        results = []
        for batch in tqdm(batches, desc="Processing batches"):
            batch_results = process_batch(ftct, batch, args.max_operations)
            results.extend(batch_results)
        
        # 
        print("\nSaving results...")
        save_ftct_format(results, output_path)
        print("Done!")

    if args.debug:
        ftct.save_responses_log()

if __name__ == "__main__":
    main()