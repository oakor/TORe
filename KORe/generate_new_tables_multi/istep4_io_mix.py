import json
import os
import random

count_indomain = 300
count_outdomain = 100

for task_id in range(1, 9):
    random.seed(task_id)
    # Define paths
    source_file_indomain = f'{source_file_root}/qa_with_reasoning_{task_id}.json'
    source_file_outdomain = f'{source_file_root}/qa_with_reasoning_{task_id}_gaps.json'
    target_file = f'{target_file_root}/train.json'
    output_file = f'{output_file_root}/ftct_train_{task_id}_i300_o100.json'

    # Read source data
    with open(source_file_indomain, 'r', encoding='utf-8') as f:
        source_data_indomain = json.load(f)
    with open(source_file_outdomain, 'r', encoding='utf-8') as f:
        source_data_outdomain = json.load(f)
    temp_data_indomain = []
    for data in source_data_indomain:
        try:
            if data["answer"].strip() == data['output'].split("Final Answer:")[1].split("</Answer>")[0].strip():
                temp_data_indomain.append(data)
        except:
            continue
    
    try:
        source_data_indomain = random.sample(temp_data_indomain, count_indomain)
        print("get {} indomain data".format(len(source_data_indomain)))
    except:
        print("No enough data : {}".format(len(temp_data_indomain)))
        raise ValueError("No enough data")

    temp_data_outdomain = []
    for data in source_data_outdomain:
        try:
            if data["answer"].strip() == data['output'].split("Final Answer:")[1].split("</Answer>")[0].strip():
                temp_data_outdomain.append(data)
        except:
            continue

    try:
        source_data_outdomain = random.sample(temp_data_outdomain, count_outdomain)
        print("get {} outdomain data".format(len(source_data_outdomain)))
    except:
        print("No enough data : {}".format(len(temp_data_outdomain)))
        raise ValueError("No enough data")

    source_data = source_data_indomain + source_data_outdomain

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