import os
import json
import torch
import argparse
import re
from tqdm import tqdm
from vllm import LLM, SamplingParams
import random

generate_qa_prompt = """
You are a table analyst. Your task is to generate question-answer pairs based on table content.

You must write the question-answer pairs in the following format:
<Question>[Your question]</Question><Answer>[Your answer]</Answer>

Here are some examples of questions and their answers:

##Example 1:
Table in json format: [table_example1]
Question: [question_example1]
Answer: [answer_example1]

##Example 2:
Table in json format: [table_example2]
Question: [question_example2]
Answer: [answer_example2]

##Example 3:
Table in json format: [table_example3]
Question: [question_example3]
Answer: [answer_example3]

##Your turn:
Table in json format: [table]
Question: 
"""

def load_train_data(train_file):
    """
    Load examples from the training data
    """
    with open(train_file, 'r', encoding='utf-8') as f:
        train_data = json.load(f)
    
    return train_data

def load_tables(train_file):
    """
    Load the tables from the training data
    """
    with open(train_file, 'r', encoding='utf-8') as f:
        train_data = json.load(f)

    tables = {}
    for item in train_data:
        tables[item["id"]] = item["instruction"].split("##Instruction:")[-1].strip()
    
    return tables

def create_prompt(table, examples):
    prompt = generate_qa_prompt.replace("[table]", table)

    for i, example in enumerate(examples):
        prompt = prompt.replace(f"[table_example{i+1}]", example["instruction"].split("##Instruction:")[-1].strip())
        prompt = prompt.replace(f"[question_example{i+1}]", example["input"].replace("###Input:", "").replace("###Response:", "").strip())
        prompt = prompt.replace(f"[answer_example{i+1}]", example["output"].strip())

    return prompt

def process_with_llm(llm, sampling_params, prompts):
    """
    Process prompts with the language model
    """
    # Prepare messages for each prompt
    messages = []
    for prompt in prompts:
        message = [
            {
                "role": "user",
                "content": prompt
            }
        ]
        messages.append(message)
    
    # Get outputs from the model
    outputs = llm.chat(messages, sampling_params=sampling_params)
    
    # Extract the generated text
    generated_texts = []
    for output in outputs:
        generated_text = output.outputs[0].text
        generated_texts.append(generated_text)
    
    return generated_texts

def save_processed_data(data, output_file):
    """
    Save the processed data with added reasoning chains
    """
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def main():
    parser = argparse.ArgumentParser(description='Add reasoning chains to QA pairs')
    parser.add_argument('--output_file', help='Path to output data')
    parser.add_argument('--prompt_file', help='Path to output dir')
    parser.add_argument('--train_file', help='Path to training data')
    parser.add_argument('--model_path', help='Path to the model')
    parser.add_argument('--batch_size', type=int, default=8, help='Batch size for processing')
    parser.add_argument('--num_examples', type=int, default=3, help='Number of examples to use for few-shot prompting')
    parser.add_argument('--target_data_counts', type=int, default=500, help='Maximum number of data to generate')
    parser.add_argument('--start_task_id', type=int, default=0, help='Start task id')
    parser.add_argument('--end_task_id', type=int, default=0, help='End task id')
    
    args = parser.parse_args()
    
    # Initialize the model
    print(f"Loading model from {args.model_path}...")
    llm = LLM(model=args.model_path, tensor_parallel_size=2, max_model_len=8000)
    sampling_params = SamplingParams(temperature=0.1, top_p=0.95, max_tokens=2048)
    
    # Load data
    for task_id in range(args.start_task_id, args.end_task_id + 1):
        task_train_file = args.train_file.replace("task_0", f"task_{task_id}")
        task_output_file = args.output_file.replace("task_0", f"task_{task_id}")
        task_prompt_file = args.prompt_file.replace("task_0", f"task_{task_id}")
        print(f"Loading data for task {task_id}...")
        data = load_train_data(task_train_file)
        tables = load_tables(task_train_file)
        print(f"Loaded {len(data)} items, {len(tables)} tables")
    
        # Process data in batches
        all_processed = []
        results = []
        while len(all_processed) < args.target_data_counts:
            for i in tqdm(range(0, len(tables), args.batch_size)):
                batch = list(tables.values())[i:i+args.batch_size]
                examples_selected = random.sample(data, args.num_examples)
            
                prompts = []
                for item in batch:
                    prompt = create_prompt(
                        table=item,
                        examples=examples_selected
                    )
                    prompts.append(prompt)
                
                with open(task_prompt_file, 'a', encoding='utf-8') as f:
                    for prompt in prompts:
                        f.write(prompt + "\n")
            
                # Process with LLM
                results = process_with_llm(llm, sampling_params, prompts)
                
                # Add reasoning to items
                for j, (item, result) in enumerate(zip(batch, results)):
                    all_processed.append({
                        "table" : item,
                        "result" : result
                        })
            
                # Free up memory
                torch.cuda.empty_cache()
        
        # Save final results
        save_processed_data(all_processed, task_output_file)
        print(f"Processed {len(all_processed)} items and saved to {task_output_file}")

if __name__ == "__main__":
    main() 
