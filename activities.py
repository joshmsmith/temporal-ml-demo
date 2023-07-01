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
class UserSentimentInput:
    filepath: str
    labels: list[str]

@dataclass
class UserSentimentOutput:
    sentiment: list[str]

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

    prediction = input.candidate_labels[np.argmax(sim)]
    probability = round(100 * sim[input.candidate_labels.index(prediction)])

    output = InferenceOutput(
        prediction = prediction,
        probability = probability
    )   
    
    return output

@activity.defn
async def get_user_sentiment(input: UserSentimentInput) -> UserSentimentOutput:
    openai.api_key = os.getenv("CHATGPT_API_KEY")

    datafile_path = input.filepath
    df = pd.read_csv(datafile_path)
    df = df[0:10]
    df

    #labels = ['negative', 'positive']

    label_embeddings = [openai.Embedding.create(input=[i], model='text-embedding-ada-002')['data'][0]['embedding'] for i in input.labels]

    pred = []
    for j in range(df.shape[0]):
        text_tester = df.Text.iloc[j]
        test_embedding = openai.Embedding.create(input=[text_tester], model='text-embedding-ada-002')['data'][0]['embedding']
        sim = [cosine_similarity(test_embedding, i) for i in label_embeddings]
        pred.append(input.labels[np.argmax(sim)])

    cols = list(df.columns)
    df = pd.concat([df, pd.Series(pred)], axis=1)
    df.columns = np.concatenate((cols, ['zeroshot']), axis=0)
    df

    output = UserSentimentOutput(
        sentiment=pred
    )
    return output        

