import json
import os
import random
import numpy as np
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

count_indomain = 400
count_outdomain = 0

# ，
def cluster_and_select(data, count, instructions, multi_instructions=None, is_multi_table=False, data_type='indomain'):
    if len(data) <= count:
        return data

    # ：instructioninput
    texts = []
    for item in data:
        # outdomain，instruction
        if data_type == 'outdomain':
            use_multi = should_use_multi_instruction(item, is_multi_table)
            if use_multi and item['id'] in multi_instructions:
                instruction = multi_instructions[item['id']]
            else:
                # instructioninstruction
                if is_multi_table and item['id'] in multi_instructions and 'filled_chains' in item:
                    multi_instruction = multi_instructions[item['id']]
                    table_json_str = multi_instruction.split('##Instruction:')[1].strip() if '##Instruction:' in multi_instruction else ""
                    single_table_json = get_single_table_from_multi(item['filled_chains'], table_json_str)
                    instruction = multi_instruction.replace(table_json_str, single_table_json)
                else:
                    instruction = instructions[item['id']]
        else:
            # indomain，instruction
            instruction = instructions[item['id']]

        input_text = item['question']
        combined_text = instruction + " " + input_text
        texts.append(combined_text)
    
    # TF-IDF
    vectorizer = TfidfVectorizer(max_features=1000)
    X = vectorizer.fit_transform(texts)
    
    # （）
    actual_clusters = min(count, len(data))
    
    # K-means
    kmeans = KMeans(n_clusters=actual_clusters, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(X)
    
    # 
    centers = kmeans.cluster_centers_
    
    # 
    selected_indices = []
    for i in range(actual_clusters):
        cluster_indices = np.where(clusters == i)[0]
        if len(cluster_indices) == 0:
            continue
            
        # 
        cluster_samples = X[cluster_indices]
        center = centers[i].reshape(1, -1)
        similarities = cosine_similarity(cluster_samples, center)
        
        # （）
        most_similar_idx = cluster_indices[np.argmax(similarities)]
        selected_indices.append(most_similar_idx)
    
    # ，
    if len(selected_indices) < count:
        remaining_indices = list(set(range(len(data))) - set(selected_indices))
        additional_indices = random.sample(remaining_indices, min(count - len(selected_indices), len(remaining_indices)))
        selected_indices.extend(additional_indices)
    
    # 
    return [data[i] for i in selected_indices]

def recognize_single_multi(json_table):
    standard_table = json.loads(json_table)
    if len(standard_table) == 1:
        return "single"
    else:
        return "multi"

def should_use_multi_instruction(data_item, is_multi_table):
    """
    instruction
    gpt4o_ostep.py：

    (is_multi_table=True):
    - f_stitch_tablesselect_table，instruction（train.jsoninstruction）
    - instructioninstruction

    (is_multi_table=False):
    - f_stitch_tablesselect_table，instruction（train_multi.json）
    - instruction（train.json）
    """
    # chain
    if 'chain' not in data_item or not data_item['chain']:
        return False

    # 
    first_operation = data_item['chain'][0].split("(")[0]

    # f_stitch_tablesselect_table，instruction
    return first_operation in ["f_stitch_tables", "select_table"]

def get_single_table_from_multi(operations, table_json_str):
    """
    instructioninstruction
    gpt4o_ostep.pyget_single_table_from_multi
    """
    try:
        standard_table = json.loads(table_json_str)
        if not isinstance(standard_table, list) or len(standard_table) == 0:
            return table_json_str

        table_0 = standard_table[0]
        table_1 = standard_table[1] if len(standard_table) > 1 else {}

        if "columns" not in table_1:
            return json.dumps({
                "columns": table_0["columns"],
                "data": table_0["data"]
            })

        output = ""
        for filled_operation in operations:
            op = filled_operation["operation"]
            cols = op.split("(")[-1].split(")")[0].split(",")
            cols = [col.strip() for col in cols]

            # table_0table_1
            if all(col in table_0["columns"] for col in cols) and not all(col in table_1["columns"] for col in cols):
                output = {
                    "columns": table_0["columns"],
                    "data": table_0["data"]
                }
                break
            # table_1table_0
            if all(col in table_1["columns"] for col in cols) and not all(col in table_0["columns"] for col in cols):
                output = {
                    "columns": table_1["columns"],
                    "data": table_1["data"]
                }
                break

        if output == "":
            if "columns" in table_1:
                # 
                import random
                output = random.choice([{
                    "columns": table_0["columns"],
                    "data": table_0["data"]
                }, {
                    "columns": table_1["columns"],
                    "data": table_1["data"]
                }])
            else:
                output = {
                    "columns": table_0["columns"],
                    "data": table_0["data"]
                }

        return json.dumps(output)
    except Exception as e:
        print(f"Error in get_single_table_from_multi: {e}")
        return table_json_str

multi_task = [1,0,0,1,0,1,0,1,1]

for task_id in range(1, 9):
    random.seed(task_id)
    # Define paths
    source_file_indomain = f'{source_file_root}/qa_with_reasoning_{task_id}.json'
    source_file_outdomain = f'{source_file_root}/qa_with_reasoning_{task_id}_gaps.json'
    target_file = f'{target_file_root}/train.json'
    output_file = f'{output_file_root}/ftct_train_{task_id}_i400_o0.json'
    
    is_multi_table = multi_task[task_id]

    # Read source data
    with open(source_file_indomain, 'r', encoding='utf-8') as f:
        source_data_indomain = json.load(f)
    with open(source_file_outdomain, 'r', encoding='utf-8') as f:
        source_data_outdomain = json.load(f)
    
    # Read target data to get instructions
    with open(target_file, 'r', encoding='utf-8') as f:
        target_data = json.load(f)

    instructions = {}
    multi_instructions = {}
    single_instructions_from_multi = {}

    if is_multi_table:
        # ：train.jsoninstruction
        for item in target_data:
            multi_instructions[item['id']] = item['instruction']
        # ，instruction
        # instruction，
        instructions = multi_instructions.copy()
    else:
        # ：train.jsoninstruction，train_multi.jsoninstruction
        for item in target_data:
            instructions[item['id']] = item['instruction']

        # instruction
        target_multi_file = target_file.replace('train.json', 'train_multi.json')
        if os.path.exists(target_multi_file):
            with open(target_multi_file, 'r', encoding='utf-8') as f:
                target_multi_data = json.load(f)
            for item in target_multi_data:
                multi_instructions[item['id']] = item['instruction']
        
    temp_data_indomain = []
    for data in source_data_indomain:
        try:
            if data["answer"].strip() == data['output'].split("Final Answer:")[1].split("</Answer>")[0].strip():
                temp_data_indomain.append(data)
        except:
            continue
    
    if len(temp_data_indomain) < count_indomain:
        print("No enough indomain data: {}".format(len(temp_data_indomain)))
        raise ValueError("No enough indomain data")
    
    # indomain
    if count_indomain > 0:
        source_data_indomain = cluster_and_select(temp_data_indomain, count_indomain, instructions,
                                                multi_instructions, is_multi_table, 'indomain')
        print("get {} indomain data".format(len(source_data_indomain)))
    else:
        source_data_indomain = []

    temp_data_outdomain = []
    for data in source_data_outdomain:
        try:
            if data["answer"].strip() == data['output'].split("Final Answer:")[1].split("</Answer>")[0].strip():
                temp_data_outdomain.append(data)
        except:
            continue

    # outdomain，indomain
    actual_count_outdomain = min(len(temp_data_outdomain), count_outdomain)
    shortage = count_outdomain - actual_count_outdomain
    
    if shortage > 0:
        print(f"Outdomain data shortage: {shortage}, will supplement from indomain data")
        # indomainshortage
        additional_count_indomain = count_indomain + shortage
        if len(temp_data_indomain) >= additional_count_indomain:
            source_data_indomain = cluster_and_select(temp_data_indomain, additional_count_indomain, instructions,
                                                    multi_instructions, is_multi_table, 'indomain')
        else:
            print(f"Warning: Not enough total data to supplement. Using all available indomain data.")
            source_data_indomain = temp_data_indomain
    else:
        # ，indomain
        if count_indomain > 0:
            source_data_indomain = cluster_and_select(temp_data_indomain, count_indomain, instructions,
                                                    multi_instructions, is_multi_table, 'indomain')
        else:
            source_data_indomain = []
    
    print("get {} indomain data".format(len(source_data_indomain)))
    
    # outdomain
    if actual_count_outdomain > 0:
        source_data_outdomain = cluster_and_select(temp_data_outdomain, actual_count_outdomain, instructions,
                                                 multi_instructions, is_multi_table, 'outdomain')
        print("get {} outdomain data".format(len(source_data_outdomain)))
    else:
        source_data_outdomain = []
        print("No outdomain data available")

    source_data = source_data_indomain + source_data_outdomain

    # Convert source data to target format
    converted_data = []
    for item in source_data:
        # outdomain，instruction
        item_instruction = instructions[item['id']]  # instruction

        # outdomaininstruction
        if item in source_data_outdomain:
            use_multi = should_use_multi_instruction(item, is_multi_table)
            if use_multi and item['id'] in multi_instructions:
                item_instruction = multi_instructions[item['id']]
            else:
                # instructioninstruction
                if is_multi_table and item['id'] in multi_instructions and 'filled_chains' in item:
                    multi_instruction = multi_instructions[item['id']]
                    table_json_str = multi_instruction.split('##Instruction:')[1].strip() if '##Instruction:' in multi_instruction else ""
                    single_table_json = get_single_table_from_multi(item['filled_chains'], table_json_str)
                    item_instruction = multi_instruction.replace(table_json_str, single_table_json)

        # Create new item in target format
        new_item = {
            'id': item['id'],
            'instruction': item_instruction,
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