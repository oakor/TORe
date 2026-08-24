import os
import json
import random
import shutil
from pathlib import Path

# 
SOURCE_DIR = ""
OUTPUT_DIR = ""

def ensure_dir(directory):
    """，"""
    Path(directory).mkdir(parents=True, exist_ok=True)

def load_json_file(file_path):
    """JSON"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json_file(data, file_path):
    """JSON"""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def get_task_folders(source_dir):
    """"""
    task_folders = []
    for item in os.listdir(source_dir):
        if item.startswith('task_') and os.path.isdir(os.path.join(source_dir, item)):
            task_folders.append(item)
    return sorted(task_folders, key=lambda x: int(x.split('_')[1]))

def create_random_selection_dataset():
    """10%"""
    task_folders = get_task_folders(SOURCE_DIR)
    
    # 
    ensure_dir(OUTPUT_DIR)
    
    # 
    for i, task_folder in enumerate(task_folders):
        task_id = int(task_folder.split('_')[1])
        task_output_dir = os.path.join(OUTPUT_DIR, f"task_{task_id}")
        ensure_dir(task_output_dir)
        
        # 
        train_file = os.path.join(SOURCE_DIR, task_folder, "train.json")
        current_train_data = load_json_file(train_file)
        
        # ，
        if i == 0:
            save_json_file(current_train_data, os.path.join(task_output_dir, "train.json"))
            continue
        
        # 
        augmented_train_data = current_train_data.copy()
        
        # 10%
        for j in range(i):
            prev_task_folder = task_folders[j]
            prev_task_train_file = os.path.join(SOURCE_DIR, prev_task_folder, "train.json")
            prev_task_data = load_json_file(prev_task_train_file)
            
            # 10%
            num_samples_to_select = max(1, int(len(prev_task_data) * 0.1))
            selected_samples = random.sample(prev_task_data, num_samples_to_select)
            
            print(f" {j}  {num_samples_to_select}  {task_id}")
            
            # 
            augmented_train_data.extend(selected_samples)
        
        # 
        save_json_file(augmented_train_data, os.path.join(task_output_dir, "train.json"))
        
        print(f" {task_id} : {len(current_train_data)}")
        print(f" {task_id} : {len(augmented_train_data)}")
        print("-" * 50)

if __name__ == "__main__":
    random.seed(23)  # 
    create_random_selection_dataset()
    print("！")
