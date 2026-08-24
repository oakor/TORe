import os
import json
import random
import numpy as np
from pathlib import Path
from sklearn.cluster import KMeans
from collections import defaultdict
import torch
from transformers import AutoModel, AutoTokenizer
from tqdm import tqdm

# 
SOURCE_DIR = ""
OUTPUT_DIR = ""
SIMCSE_MODEL = ""  # SimCSE

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

class SimCSEEmbedder:
    """SimCSE"""
    def __init__(self, model_name_or_path):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)
        self.model = AutoModel.from_pretrained(model_name_or_path)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        self.model.eval()
        print(f"SimCSE model loaded on {self.device}")

    def encode(self, sentences, batch_size=32):
        """"""
        all_embeddings = []
        
        for i in range(0, len(sentences), batch_size):
            batch_sentences = sentences[i:i+batch_size]
            inputs = self.tokenizer(batch_sentences, padding=True, truncation=True, return_tensors="pt")
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            with torch.no_grad():
                outputs = self.model(**inputs, output_hidden_states=True, return_dict=True)
                # [CLS]
                embeddings = outputs.pooler_output
                all_embeddings.append(embeddings.cpu().numpy())
        
        return np.vstack(all_embeddings)

def extract_text_for_embedding(data):
    """"""
    texts = []
    for item in data:
        # 
        text = item.get('instruction', '') + ' ' + item.get('input', '') + ' ' + item.get('output', '')
        texts.append(text)
    return texts

def select_samples_by_kmeans(data, embedder, percentage=0.1, n_clusters=20):
    """K-means"""
    if len(data) == 0:
        return []
    
    # 
    texts = extract_text_for_embedding(data)
    
    # SimCSE
    print(f"{len(texts)}...")
    features = embedder.encode(texts)
    
    # ，20，
    n_clusters = min(n_clusters, len(data))
    
    print(f"K-means，: {n_clusters}...")
    # K-means
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    cluster_labels = kmeans.fit_predict(features)
    
    # 
    distances = []
    for i, label in enumerate(cluster_labels):
        center = kmeans.cluster_centers_[label]
        distance = np.linalg.norm(features[i] - center)
        distances.append((i, distance))
    
    # 
    clusters = defaultdict(list)
    for i, label in enumerate(cluster_labels):
        clusters[label].append(i)
    
    # 
    selected_indices = []
    total_samples_to_select = max(1, int(len(data) * percentage))
    
    # 
    samples_per_cluster = total_samples_to_select // n_clusters
    remainder = total_samples_to_select % n_clusters
    
    for label in range(n_clusters):
        cluster_indices = clusters[label]
        # 
        n_select = samples_per_cluster + (1 if label < remainder else 0)
        n_select = min(n_select, len(cluster_indices))
        
        # 
        cluster_distances = [(i, distances[i][1]) for i in cluster_indices]
        # 
        cluster_distances.sort(key=lambda x: x[1])
        # 
        selected_indices.extend([idx for idx, _ in cluster_distances[:n_select]])
    
    print(f"{len(selected_indices)}")
    # 
    return [data[i] for i in selected_indices]

def create_kmeans_selection_dataset():
    """K-means"""
    task_folders = get_task_folders(SOURCE_DIR)
    
    # 
    ensure_dir(OUTPUT_DIR)
    
    # SimCSE
    embedder = SimCSEEmbedder(SIMCSE_MODEL)
    
    # 
    for i, task_folder in enumerate(task_folders):
        if i in [7, 8]:
            continue
        task_id = int(task_folder.split('_')[1])
        task_output_dir = os.path.join(OUTPUT_DIR, f"task_{task_id}")
        ensure_dir(task_output_dir)
        
        print(f" {task_id}...")
        
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
            prev_task_id = int(prev_task_folder.split('_')[1])
            prev_task_train_file = os.path.join(SOURCE_DIR, prev_task_folder, "train.json")
            prev_task_data = load_json_file(prev_task_train_file)
            
            print(f" {prev_task_id}  {task_id}...")
            
            # SimCSEK-means10%
            selected_samples = select_samples_by_kmeans(prev_task_data, embedder, percentage=0.1, n_clusters=20)
            
            print(f" {prev_task_id}  {len(selected_samples)}  {task_id}")
            
            # 
            augmented_train_data.extend(selected_samples)
        
        # 
        save_json_file(augmented_train_data, os.path.join(task_output_dir, "train.json"))
        
        print(f" {task_id} : {len(current_train_data)}")
        print(f" {task_id} : {len(augmented_train_data)}")
        print("-" * 50)

if __name__ == "__main__":
    np.random.seed(22)  # 
    random.seed(22)  # 
    create_kmeans_selection_dataset()
    print("！")
