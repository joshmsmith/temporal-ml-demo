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