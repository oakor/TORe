import json
import os
import random

for task_id in range(9):
    random.seed(task_id)
    # Define paths
    source_file = f'{source_file_root}/qa_with_reasoning_{task_id}.json'
    target_file = f'{target_file_root}/train.json'
    output_file = f'{output_file_root}/indomain_train_{task_id}.json'

    # Read source data
    with open(source_file, 'r', encoding='utf-8') as f:
        source_data = json.load(f)
    temp_data = []
    for data in source_data:
        try:
            if data["answer"].strip() == data['output'].split("Final Answer:")[1].split("</Answer>")[0].strip():
                temp_data.append(data)
        except:
            continue
    
    try:
        source_data = random.sample(temp_data, 400)
    except:
        print("No enough data : {}".format(len(temp_data)))
        raise ValueError("No enough data")

    # Read target data
    with open(target_file, 'r', encoding='utf-8') as f:
        target_data = json.load(f)

    instructions = {}
    for item in target_data:
        instructions[item['id']] = item['instruction']

    # Create the instruction template from target data
    instruction_template = target_data[0]['instruction']

    # Convert source data to target format
    converted_data = []
    for item in source_data:
        # Create new item in target format
        new_item = {
            'id': item['id'],
            'instruction': instructions[item['id']],
            'input': f"###Input:\n{item['question']}\n\n###Response:",
            'output': item['output'].split("<Reasoning>")[1].split("</Reasoning>")[0] + "\n\nFinal Answer: " + item['output'].split("Final Answer:")[1].split("</Answer>")[0]
        }
        converted_data.append(new_item)

    # Merge data
    merged_data = target_data + converted_data

    # Write merged data to output file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(merged_data, f, ensure_ascii=False, indent=4)

    print(f"Conversion and merge complete. Output saved to {output_file}")
    print(f"Original train.json has {len(target_data)} items")
    print(f"Converted qa_with_reasoning.json has {len(converted_data)} items")
    print(f"Merged file has {len(merged_data)} items") 