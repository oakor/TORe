import os, json

target_dir = ""
input_dir = ""

os.makedirs(target_dir, exist_ok=True)

for task_id in range(9):
    task_dir = os.path.join(input_dir, f"task_{task_id}")
    train_file = os.path.join(task_dir, "train.json")
    with open(train_file, "r") as f:
        train_data = json.load(f)
    
    output_file = os.path.join(target_dir, f"stream2_multi_table_task_{task_id}_KmeansSel_10.json")
    with open(output_file, "w") as f:
        json.dump(train_data, f, ensure_ascii=False, indent=4)

print("Transfer completed!")