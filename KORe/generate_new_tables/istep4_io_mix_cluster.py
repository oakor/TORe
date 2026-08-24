import json
import os
import random
import numpy as np
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

count_indomain = 300
count_outdomain = 100

# ，
def cluster_and_select(data, count, instructions):
    if len(data) <= count:
        return data
    
    # ：instructioninput
    texts = []
    for item in data:
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
        
        #
        most_similar_idx = cluster_indices[np.argmax(similarities)]
        selected_indices.append(most_similar_idx)
    
    #
    if len(selected_indices) < count:
        remaining_indices = list(set(range(len(data))) - set(selected_indices))
        additional_indices = random.sample(remaining_indices, min(count - len(selected_indices), len(remaining_indices)))
        selected_indices.extend(additional_indices)
    
    # 
    return [data[i] for i in selected_indices]

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
    
    # Read target data to get instructions
    with open(target_file, 'r', encoding='utf-8') as f:
        target_data = json.load(f)

    instructions = {}
    for item in target_data:
        instructions[item['id']] = item['instruction']
        
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
        source_data_indomain = cluster_and_select(temp_data_indomain, count_indomain, instructions)
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

    if len(temp_data_outdomain) < count_outdomain:
        print("No enough outdomain data: {}".format(len(temp_data_outdomain)))
        raise ValueError("No enough outdomain data")
    
    # outdomain
    if count_outdomain > 0:
        source_data_outdomain = cluster_and_select(temp_data_outdomain, count_outdomain, instructions)
        print("get {} outdomain data".format(len(source_data_outdomain)))
    else:
        source_data_outdomain = []

    source_data = source_data_indomain + source_data_outdomain

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