import os
import json
import torch
import argparse
import re
from tqdm import tqdm
from vllm import LLM, SamplingParams
import random

generate_reasoning_prompt = """
You are a table analyst. Your task is to write a reasoning chain of thought to answer questions based on table content.

You must write the reasoning chain of thought in the following format:
<Reasoning>[Your reasoning chain of thought]</Reasoning><Answer>Final Answer:[Your final answer]</Answer>

Here are some examples of questions and their reasoning chains of thought:

##Example 1:
Table in json format: [table_example1]
Question: [question_example1]
Answer: [answer_example1]
Reasoning: [reasoning_example1]

##Example 2:
Table in json format: [table_example2]
Question: [question_example2]
Answer: [answer_example2]
Reasoning: [reasoning_example2]

##Example 3:
Table in json format: [table_example3]
Question: [question_example3]
Answer: [answer_example3]
Reasoning: [reasoning_example3]

##Your turn:
Table in json format: [table]
Question: [question]
Answer: [answer]
Reasoning:
"""

def load_data(input_file):
    """
    Load the generated QA pairs from istep1
    """
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

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

def extract_table_by_id(train_file, table_id):
    """
    Extract a table from the training data by its ID
    """
    with open(train_file, 'r', encoding='utf-8') as f:
        train_data = json.load(f)
    
    for item in train_data:
        if item["id"] == table_id:
            # Extract the table from the instruction field
            instruction = item["instruction"]
            match = re.search(r'##Instruction:(.*?)(?=\n\n|$)', instruction, re.DOTALL)
            if match:
                table_json_str = match.group(1).strip()
                try:
                    return json.loads(table_json_str)
                except Exception as e:
                    print(f"Error parsing table JSON for ID {table_id}: {e}")
                    pass
    return None

def create_prompt(question, answer, table, examples):
    prompt = generate_reasoning_prompt.replace("[table]", table)
    prompt = prompt.replace("[question]", question)
    prompt = prompt.replace("[answer]", answer)

    for i, example in enumerate(examples):
        prompt = prompt.replace(f"[table_example{i+1}]", example["instruction"].split("##Instruction:")[-1].strip())
        prompt = prompt.replace(f"[question_example{i+1}]", example["input"].replace("###Input:", "").replace("###Response:", "").strip())
        prompt = prompt.replace(f"[answer_example{i+1}]", example["output"].split("Final Answer:")[-1].split("\n")[0].split("```")[0].strip())
        prompt = prompt.replace(f"[reasoning_example{i+1}]", "<Reasoning>" + example["output"].split("Final Answer:")[0].strip() + "</Reasoning>" + "<Answer>Final Answer:" + example["output"].split("Final Answer:")[-1].split("\n")[0].split("```")[0].strip() + "</Answer>")

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
    parser.add_argument('--input_file', help='Path to input data')
    parser.add_argument('--output_file', help='Path to output data')
    parser.add_argument('--prompt_file', help='Path to output dir')
    parser.add_argument('--train_file', help='Path to training data')
    parser.add_argument('--model_path', help='Path to the model')
    parser.add_argument('--batch_size', type=int, default=8, help='Batch size for processing')
    parser.add_argument('--num_examples', type=int, default=3, help='Number of examples to use for few-shot prompting')
    
    args = parser.parse_args()
    
    # Initialize the model
    print(f"Loading model from {args.model_path}...")
    llm = LLM(model=args.model_path, tensor_parallel_size=2, max_model_len=8000)
    sampling_params = SamplingParams(temperature=0.1, top_p=0.95, max_tokens=2048)
    
    # Load data
    print("Loading data...")
    data = load_data(args.input_file)
    examples = load_train_data(args.train_file)
    tables = load_tables(args.train_file)
    print(f"Loaded {len(data)} items and {len(examples)} examples")
    
    # Process data in batches
    all_processed = []
    for i in tqdm(range(0, len(data), args.batch_size)):
        batch = data[i:i+args.batch_size]
        
        if len(examples) >= args.num_examples:
            examples_selected = random.sample(examples, args.num_examples)
        else:
            examples_selected = examples
        
        # Create prompts for the batch
        prompts = []
        for item in batch:
            prompt = create_prompt(
                question=item["question"],
                answer=item["answer"],
                table=tables[item["id"]],
                examples=examples_selected
            )
            prompts.append(prompt)
        
        with open(args.prompt_file, 'a', encoding='utf-8') as f:
            for prompt in prompts:
                f.write(prompt + "\n")
        
        # Process with LLM
        results = process_with_llm(llm, sampling_params, prompts)
        
        # Add reasoning to items
        for j, (item, result) in enumerate(zip(batch, results)):
            item["output"] = result
            all_processed.append(item)
        
        # Free up memory
        torch.cuda.empty_cache()
        
        # Save intermediate results
        if i % 50 == 0 and i > 0:
            save_processed_data(all_processed, args.output_file + f".part_{i}")
    
    # Save final results
    save_processed_data(all_processed, args.output_file)
    print(f"Processed {len(all_processed)} items and saved to {args.output_file}")

if __name__ == "__main__":
    main() 