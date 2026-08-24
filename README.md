# Code for Knowledge Base Operation Recipe: A Knowledge Reconstruction Framework for KBQA Continual Learnin

## Data

This project need four public dataset. Here we provide the source of the datasets.
SQUALL: https://opendatalab.com/OpenDataLab/squall
TableInstruct: https://huggingface.co/datasets/Multilingual-Multimodal-NLP/TableInstruct
MMQA: https://anonymous.4open.science/r/MMQA-34B1
OmniSQL: https://github.com/RUCKBReasoning/OmniSQL

You could download them and change the path_to_data parameter lead th them in KORe files.

## Method

Please refer to README.md in KORe directory.

## Baselines

We list five baselines used in our paper, you could find others in the paper we referred to. 

Baselines in the 'Baselines' directory include MTL, vanilla, KmeansSel, RandomSel and naive_generate, you could run them directly.

## Evaluate

We provide the evaluate code we used in our experiment. You could find them in the 'evaluate' directory.
