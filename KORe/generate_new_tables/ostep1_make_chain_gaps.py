import json
import os
from tqdm import tqdm
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--root_input_path", type=str)
parser.add_argument("--root_output_path", type=str)
args = parser.parse_args()
root_input_path = args.root_input_path
root_output_path = args.root_output_path

for task_id in tqdm(range(9)):
    chain_file = os.path.join(root_input_path, f"processed_chains_{task_id}.json")
    with open(chain_file, "r") as f:
        chains_data = json.load(f)
    
    chains_now = set()
    for chain_data in chains_data:
        chain = " ".join(chain_data["chain"])
        chains_now.add(chain)
    
    former_chains = {}
    for former_id in range(task_id):
        former_chain_file = os.path.join(root_input_path, f"processed_chains_{former_id}.json")
        with open(former_chain_file, "r") as f:
            former_chains_data = json.load(f)
        
        for chain_data in former_chains_data:
            chain = " ".join(chain_data["chain"])
            former_chains[chain] = chain_data
    
    chains_gaps = []
    for chain_former in tqdm(list(former_chains.keys())):
        if chain_former not in chains_now:
            chains_gaps.append(former_chains[chain_former])
    
    with open(os.path.join(root_output_path, f"processed_chains_{task_id}_gaps.json"), "w") as f:
        json.dump(chains_gaps, f, indent=4)
