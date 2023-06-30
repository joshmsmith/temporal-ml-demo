import pandas as pd
pd.set_option('display.max_colwidth', 0)

import numpy as np
import openai
import os
from openai.embeddings_utils import cosine_similarity, get_embedding

from transformers import pipeline

from dataclasses import dataclass
from temporalio import activity

@dataclass
class InferenceInput:
    sequence: str
    candidate_labels: list[str]

@dataclass
class InferenceOutput:
    prediction: str
    probability: int

@activity.defn
async def get_available_task_queue() -> str:
    raise NotImplementedError

@activity.defn
async def get_best_label(input: InferenceInput) -> InferenceOutput:
    openai.api_key = os.getenv("CHATGPT_API_KEY")

    label_embeddings = [openai.Embedding.create(input=[i], model='text-embedding-ada-002')['data'][0]['embedding'] for i in input.candidate_labels]
    test_embedding = openai.Embedding.create(input=[input.sequence], model='text-embedding-ada-002')['data'][0]['embedding']

    sim = [cosine_similarity(test_embedding, i) for i in label_embeddings]
    print('sim: ', sim)

    prediction = input.candidate_labels[np.argmax(sim)]
    probability = round(100 * sim[input.candidate_labels.index(prediction)])
    print('prediction: ', prediction, probability)

    output = InferenceOutput(
        prediction = prediction,
        probability = probability
    )   
    
    return output

@activity.defn
async def update_rating():
    openai.api_key = os.getenv("CHATGPT_API_KEY")

    datafile_path = 'dataset/reviews.csv'
    df = pd.read_csv(datafile_path)
    df = df[0:10]
    df

    labels = ['negative', 'positive']

    label_embeddings = [openai.Embedding.create(input=[i], model='text-embedding-ada-002')['data'][0]['embedding'] for i in labels]

    pred = []
    for j in range(df.shape[0]):
        text_tester = df.Text.iloc[j]
        print("\n")
        print(text_tester)
        test_embedding = openai.Embedding.create(input=[text_tester], model='text-embedding-ada-002')['data'][0]['embedding']
        sim = [cosine_similarity(test_embedding, i) for i in label_embeddings]
        print("\n")
        print(labels[np.argmax(sim)])
        pred.append(labels[np.argmax(sim)])

    cols = list(df.columns)
    df = pd.concat([df, pd.Series(pred)], axis=1)
    df.columns = np.concatenate((cols, ['zeroshot']), axis=0)
    df

    TP = 0
    TN = 0
    FP = 0
    FN = 0
    for i in range(len(df)):
        if df.Score.iloc[i] > 3 and df.zeroshot.iloc[i] == 'positive':
            TP = TP + 1
        elif df.Score.iloc[i] < 3 and df.zeroshot.iloc[i] == 'negative':
            TN = TN + 1
        elif df.Score.iloc[i] > 3 and df.zeroshot.iloc[i] == 'negative':
            FP = FP + 1
        elif df.Score.iloc[i] < 3 and df.zeroshot.iloc[i] == 'positive':
            FN = FN + 1
    accuracy = (TP + TN)/(TP + TN + FP + FN)
    print('accuracy: ', accuracy, pred)        