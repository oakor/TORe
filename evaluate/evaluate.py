import argparse
import os
import numpy as np
import json
from tqdm import tqdm
from collections import defaultdict

def normalize_answer(s):
    """Normalize the answer string for comparison."""
    if not s:
        return ""
    s = s.lower().strip()
    return s

def exact_match(references, candidate):
    """Check if the candidate matches any of the references."""
    if not candidate:
        return False
    for reference in references:
        if normalize_answer(reference) == normalize_answer(candidate):
            return True
    return False

def clean_answer(answer):
    """Extract the final answer from text."""
    if "Final Answer:" in answer:
        if len(answer.split("Final Answer:")) >= 3:
            return answer.split("Final Answer:")[-2].split("\n")[0].split("```")[0].strip()
        else:
            return answer.split("Final Answer:")[1].split("\n")[0].split("```")[0].strip()
    return answer.strip()

def process_results(source_path, target_path, task_num):
    """Process the inference results to prepare for evaluation."""
    if not os.path.exists(os.path.join(target_path, "processed")):
        os.makedirs(os.path.join(target_path, "processed"))
    
    for task_id in range(task_num):
        test_all = min(task_id + 2, task_num) if task_id < task_num - 1 else task_num
        for test_on in range(test_all):
            source_file = os.path.join(source_path, f"task_{test_on}", "test.json")
            target_file = os.path.join(target_path, f"task_{task_id}_test_{test_on}.json")
            
            if not os.path.exists(target_file):
                print(f"Warning: {target_file} does not exist, skipping...")
                continue
                
            source_datas, target_datas = [], []
            with open(source_file, 'r') as fp:
                source_datas = json.load(fp)
            with open(target_file, 'r') as fp:
                target_datas = json.load(fp)
            
            outputs = []
            for target in target_datas:
                target["predict"] = target["generate"]
                target["generate"] = clean_answer(target["generate"])
                target["answer"] = clean_answer(target["output"])
                outputs.append(target)
            
            processed_file = os.path.join(target_path, "processed", f"task_{task_id}_test_on_{test_on}.json")
            with open(processed_file, 'w') as fp:
                json.dump(outputs, fp)
            print(f"Processed file saved to {processed_file}")
    
    return os.path.join(target_path, "processed")

def evaluate_one_task(path):
    """Evaluate a single task file."""
    with open(path, 'r') as fp:
        datas = json.load(fp)
    
    right, all_count = 0, 0
    for data in datas:
        reference_answer = [data['answer']]
        assistant_answer = data["generate"].split("<|endoftext|>")[0]
        
        verify = exact_match(reference_answer, assistant_answer)
        right += 1 if verify else 0
        all_count += 1
    
    accuracy = right / all_count if all_count > 0 else 0
    return accuracy, all_count

def eval_stream_task(task_num, test_num, em_acc):
    """Calculate the evaluation metrics for the stream of tasks."""
    acc_avg_em = [float("-inf") for _ in range(task_num)]
    acc_whole_em = [float("-inf") for _ in range(task_num)]
    bwt_em = [float("-inf") for _ in range(task_num)]
    fwt_em = [float("-inf") for _ in range(task_num)]

    for task_id in range(task_num):
        # acc_avg AND acc_whole
        acc_avg_em[task_id] = np.mean(em_acc[task_id, 0:task_id+1])

        acc_whole_em[task_id] = np.sum(em_acc[task_id, 0:task_id+1] * np.array(list(test_num.values())[0:task_id+1])) / np.sum(np.array(list(test_num.values())[0:task_id+1]))

        # BWT AND FWT
        if task_id > 0:
            # BWT
            bwt_em_tmp = 0
            for past_id in range(task_id):
                bwt_em_tmp += em_acc[task_id][past_id] - em_acc[past_id][past_id]
            bwt_em[task_id] = bwt_em_tmp / task_id

            # FWT
            fwt_em_tmp = 0
            for i in range(task_id, -1, -1):
                fwt_em_tmp += em_acc[i-1][i]
                if i-1 == 0:
                    break
            fwt_em[task_id] = fwt_em_tmp / task_id

    stream_task_result = {
        "acc_avg_em": acc_avg_em,
        "acc_whole_em": acc_whole_em,
        "bwf_em": bwt_em,
        "fwt_em": fwt_em,
    }

    return stream_task_result

def evaluate_all_tasks(task_num, processed_path):
    """Evaluate all tasks and calculate metrics."""
    em_acc = np.zeros((task_num, task_num))
    task_test_num = {}
    
    # Store detailed results for each task
    detailed_results = defaultdict(dict)
    
    # Flag to check if any result files were found
    found_results = False
    
    for i in range(task_num):
        for j in range(min(i+2, task_num)):
            task_path = os.path.join(processed_path, f"task_{str(i)}_test_on_{str(j)}.json")
            if not os.path.exists(task_path):
                print(f"Warning: {task_path} does not exist, skipping...")
                continue
                
            found_results = True
            task_acc, example_count = evaluate_one_task(task_path)
            em_acc[i][j] = task_acc
            detailed_results[f"task_{i}"][f"test_{j}"] = task_acc
            print(f"Task {i} on Test {j}: Accuracy = {task_acc:.4f}")
            
            if j not in task_test_num:
                task_test_num[j] = example_count
    
    print('Accuracy Matrix:')
    print(em_acc)
    print('Sample Count:')
    print(task_test_num)
    
    # If no result files were found, return empty results
    if not found_results:
        print("Warning: No result files were found. Returning empty results.")
        return {
            "detailed_accuracy": {},
            "accuracy_matrix": em_acc.tolist(),
            "metrics": {
                "acc_avg_em": [0.0] * task_num,
                "acc_whole_em": [0.0] * task_num,
                "bwf_em": [0.0] * task_num,
                "fwt_em": [0.0] * task_num,
            }
        }
    
    stream_task_result = eval_stream_task(task_num, task_test_num, em_acc)
    
    # Combine detailed results with summary metrics
    final_results = {
        "detailed_accuracy": detailed_results,
        "accuracy_matrix": em_acc.tolist(),
        "metrics": stream_task_result
    }
    
    return final_results

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--results_dir', type=str)
    parser.add_argument('--data_dir', type=str)
    parser.add_argument('--output_file', type=str)
    parser.add_argument('--task_num', type=int, default=9)
    parser.add_argument('--process_results', action='store_true', 
                        help='Process raw inference results before evaluation')
    return parser.parse_args()

def main():
    args = parse_args()
    
    processed_path = args.results_dir
    if args.process_results:
        processed_path = process_results(args.data_dir, args.results_dir, args.task_num)
    
    print("Evaluating all tasks...")
    results = evaluate_all_tasks(args.task_num, processed_path)
    
    # Save the evaluation results
    with open(args.output_file, 'w') as fp:
        json.dump(results, fp, indent=2)
    
    print(f"Evaluation results saved to {args.output_file}")
    
    # Print the summary metrics
    for key, values in results["metrics"].items():
        print(f"{key}: {values}")

if __name__ == '__main__':
    main() 