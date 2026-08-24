import os
import json
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from tqdm import tqdm
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_path", type=str)
    parser.add_argument("--task_id", type=int)
    parser.add_argument("--data_dir", type=str)
    parser.add_argument("--output_dir", type=str)
    parser.add_argument("--batch_size", type=int, default=1)
    parser.add_argument("--max_new_tokens", type=int, default=512)
    parser.add_argument("--temperature", type=float, default=0.1)
    parser.add_argument("--num_samples", type=int, default=None, help="Number of samples to process (for testing)")
    return parser.parse_args()

def main():
    args = parse_args()
    
    # Check if the model path contains merged_models directory
    model_path = args.model_path
    if os.path.exists(os.path.join(model_path, "merged_models")):
        model_path = os.path.join(model_path, "merged_models")
    
    print(f"Loading model from {model_path}")
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        torch_dtype=torch.float16,
        device_map="auto"
    )
    
    # Determine which tasks to infer on based on the task_id
    task_range = range(min(args.task_id + 2, 9)) if args.task_id < 8 else range(9)
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)
    
    for test_task_id in task_range:
        print(f"Processing inference for model trained on task_{args.task_id}, testing on task_{test_task_id}")
        
        test_data_path = os.path.join(args.data_dir, f"task_{test_task_id}", "test.json")
        output_file = os.path.join(args.output_dir, f"task_{args.task_id}_test_{test_task_id}.json")
        
        print(f"Loading test data from {test_data_path}")
        with open(test_data_path, "r", encoding="utf-8") as f:
            test_data = json.load(f)
        
        if args.num_samples is not None:
            test_data = test_data[:args.num_samples]
        
        results = []
        
        # Process data in batches
        for i in tqdm(range(0, len(test_data), args.batch_size), desc=f"Processing test data for task_{test_task_id}"):
            batch = test_data[i:i + args.batch_size]
            batch_prompts = [f"{item['instruction']}\n\n{item['input']}" for item in batch]
            
            # Tokenize batch
            inputs = tokenizer(batch_prompts, return_tensors="pt", padding=True).to(model.device)
            
            # Generate
            with torch.no_grad():
                outputs = model.generate(
                    **inputs,
                    max_new_tokens=args.max_new_tokens,
                    temperature=args.temperature,
                    do_sample=args.temperature > 0,
                )
            
            # Process each item in the batch
            for j, (item, prompt, output_ids) in enumerate(zip(batch, batch_prompts, outputs)):
                # Decode the generated text
                generated_text = tokenizer.decode(output_ids, skip_special_tokens=True)
                
                # Extract the model's response (everything after the prompt)
                response = generated_text[len(prompt):]
                
                # Store the result
                result = {
                    "id": item["id"],
                    "instruction": item["instruction"],
                    "input": item["input"],
                    "output": item["output"],
                    "generate": response
                }
                results.append(result)
        
        # Save the results to the output file
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"Results saved to {output_file}")

if __name__ == "__main__":
    main() 