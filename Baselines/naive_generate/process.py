import json
import os

root_dir = ""
root_train = ""
root_output = ""

for task_id in range(9):
    file_path = os.path.join(root_dir, f"task_{task_id}_qa_pairs.json")
    file_train = os.path.join(root_train, f"task_{task_id}/train.json")
    file_output = os.path.join(root_output, f"stream2_multi_table_task_{task_id}_naive_generate.json")
    with open(file_path, "r") as f:
        data = json.load(f)
    with open(file_train, "r") as f:
        data_train = json.load(f)
    output = data_train
    Instruct = data_train[0]["instruction"].split("##Instruction:")[0] + "##Instruction:"
    for item in data:
        item_instruction = Instruct + item["table"]
        item_input = "###Input:\n" + item["result"].split("<Question>")[-1].split("</Question>")[0] + "\n\n###Response:"
        item_output = item["result"].split("<Answer>")[-1].split("</Answer>")[0]
        output.append({"instruction": item_instruction, "input": item_input, "output": item_output})
    with open(file_output, "w") as f:
        json.dump(output, f, indent=4)
