import os
from datasets import Dataset, concatenate_datasets
import pandas as pd
from transformers import DataCollatorForSeq2Seq, TrainingArguments, Trainer
import argparse
from peft import get_peft_model
from tqdm import tqdm
from train_base import Train_Base

class MTL(Train_Base):
    def __init__(self, model_path, args):
        super().__init__(model_path)
        self.model = get_peft_model(self.model, self.peft_config)
        self.model.print_trainable_parameters()
        self.args = args

    def mtl_train(self):
        os.makedirs(self.args.save_dir, exist_ok=True)
        os.makedirs(self.args.logs_dir, exist_ok=True)

        for task_id in tqdm(range(9)):
            print(f"========== Training Task {task_id} ==========")
            conbimed_ids = []
            for recall_task_id in range(task_id + 1):
                train_task_path = os.path.join(self.args.train_data, f"task_{recall_task_id}", "train.json")
                conbimed_ids.append(self.process_data(train_task_path, recall_task_id, data_type="train"))
            train_tokenized_ds = concatenate_datasets(conbimed_ids)
            train_tokenized_ds = train_tokenized_ds.shuffle(seed=22)

            dev_task_path = os.path.join(self.args.train_data, f"task_{task_id}", "dev.json")
            dev_tokenized_ds = self.process_data(dev_task_path, task_id, data_type="dev")
            
            task_log_dir = os.path.join(self.args.logs_dir, f"task_{task_id}")
            task_save_dir = os.path.join(self.args.save_dir, f"task_{task_id}")

            training_args = TrainingArguments(
                output_dir=task_log_dir,
                per_device_train_batch_size=self.args.batch_size,
                gradient_accumulation_steps=4,
                logging_steps=10,
                num_train_epochs=self.args.epoch,
                learning_rate=1e-4,
                gradient_checkpointing=True,
            )

            self.model = self.train_one_task(train_tokenized_ds, dev_tokenized_ds, self.tokenizer, self.model, training_args, task_save_dir, task_id, self.args.early_stop_patience)
        


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--train_data', type=str, required=True)
    parser.add_argument('--logs_dir', type=str, required=True)
    parser.add_argument('--batch_size', type=int, required=True)
    parser.add_argument('--epoch', type=int, required=True)
    parser.add_argument('--early_stop_patience', type=int, default=2, help='Number of evaluations to wait for improvement')
    parser.add_argument('--save_dir', type=str, required=True)
    args = parser.parse_args()

    mtl = MTL('', args)
    mtl.mtl_train()
