import json
import os
from tqdm import tqdm

chain_path = ""
output_path = ""

# 
os.makedirs(output_path, exist_ok=True)

for task_id in tqdm(range(9)):
    chain_file = os.path.join(chain_path, f"processed_chains_{task_id}.json")
    with open(chain_file, "r") as f:
        chains_data = json.load(f)
    
    chains_now = set()
    for chain_data in chains_data:
        chain = " ".join(chain_data["chain"])
        chains_now.add(chain)
    
    # ，former_idgaps
    former_gaps = {}
    
    for former_id in range(task_id):
        former_chain_file = os.path.join(chain_path, f"processed_chains_{former_id}.json")
        with open(former_chain_file, "r") as f:
            former_chains_data = json.load(f)
        
        # former_idgaps
        former_gaps[former_id] = []
        
        # gapsformer_id
        for chain_data in former_chains_data:
            chain = " ".join(chain_data["chain"])
            if chain not in chains_now:
                former_gaps[former_id].append(chain_data)
        
        # former_idgaps
        output_file = os.path.join(output_path, f"processed_chains_{former_id}_for_{task_id}_gaps.json")
        with open(output_file, "w") as f:
            json.dump(former_gaps[former_id], f, indent=4)
        
        print(f"task_{task_id}task_{former_id}{len(former_gaps[former_id])}gaps")
    
    # gaps，
    all_gaps = []
    for former_id in former_gaps:
        all_gaps.extend(former_gaps[former_id])
    
    # with open(os.path.join(output_path, f"processed_chains_{task_id}_gaps.json"), "w") as f:
    #     json.dump(all_gaps, f, indent=4)
    
    print(f"task_{task_id}{len(all_gaps)}gaps")
