import pandas as pd
pd.set_option('display.max_colwidth', 0)
import time
import numpy as np
import openai
import os
from openai.embeddings_utils import cosine_similarity, get_embedding

from transformers import pipeline

from dataclasses import dataclass
from temporalio import activity

@dataclass
class UserSentimentInput:
    filepath: str

@dataclass
class UserSentimentOutput:
    sentiment: list[str]
    probability: list[int]
    text: list[str]
    index: list[int]

@dataclass
class Signal:
    location: str
    filepath: str
    labels: list[str]

@activity.defn
async def get_available_task_queue() -> str:
    raise NotImplementedError
  
@activity.defn
async def get_location(input: UserSentimentInput) -> list[str]:
    time.sleep(2) 

    datafile_path = input.filepath
    df = pd.read_csv(datafile_path)

    return df['Reviewer_Location'].unique()
      
@activity.defn
async def get_user_sentiment(input: Signal) -> UserSentimentOutput:
    openai.api_key = os.getenv("CHATGPT_API_KEY")
    
    datafile_path = input.filepath
    df = pd.read_csv(datafile_path)

    label_embeddings = [openai.Embedding.create(input=[i], model='text-embedding-ada-002')['data'][0]['embedding'] for i in input.labels]

    pred_list = []
    probability_list = []
    text_list = []
    index_list = []

    for i, row in df.iterrows():
        if row.Reviewer_Location == input.location:
            text_tester = row.Review_Text
            test_embedding = openai.Embedding.create(input=[text_tester], model='text-embedding-ada-002')['data'][0]['embedding']
            sim = [cosine_similarity(test_embedding, i) for i in label_embeddings]

            pred_list.append(input.labels[np.argmax(sim)])
            probability_list.append(round(100 * max(sim)))
            text_list.append(text_tester)
            index_list.append(i)

    cols = list(df.columns)
    df = pd.concat([df, pd.Series(pred_list)], axis=1)
    df.columns = np.concatenate((cols, ['zeroshot']), axis=0)
    df

    output = UserSentimentOutput(
        sentiment = pred_list,
        probability = probability_list,
        text = text_list,
        index = index_list
    )
    return output        

