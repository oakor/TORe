import os
import json
import logging
from typing import List, Dict, Any

# 
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def process_chain(chain: List[str]) -> List[str]:
    """
    "skip"
    
    Args:
        chain: 
        
    Returns:
        
    """
    return [op for op in chain if not op.startswith("skip")]

def process_data(input_file: str, output_file: str):
    # 
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 
    processed_data = []
    for sample in data:
        if "chain" in sample.keys():
            # 
            processed_chain = process_chain(sample["chain"])
            if processed_chain:  # 
                sample["chain"] = processed_chain
                if sample["chain"][-1] != "END":
                    sample["chain"].append("END")
                processed_data.append(sample)
    # 
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(processed_data, f, ensure_ascii=False, indent=2)
        
    logger.info(f" {len(processed_data)} ")
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file_root", type=str)
    parser.add_argument("--output_file_root", type=str)
    args = parser.parse_args()
    input_file_root = args.input_file_root
    output_file_root = args.output_file_root
    for task_id in range(9):
        input_file = f"{input_file_root}/task_{task_id}/train.json" 
        output_file = f"{output_file_root}/processed_chains_{task_id}.json"

        process_data(input_file, output_file)