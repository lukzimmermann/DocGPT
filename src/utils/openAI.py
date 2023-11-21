import os
import openai
import tiktoken
import numpy as np
from dotenv import load_dotenv

class Embedding:
    def __init__(self):
        self.tokens = 0
        self.vector = 0

MODEL = "text-embedding-ada-002"
MAX_TOKENS = 8192

def chat(prompt: str) -> str:
  openai.organization = os.getenv("OPENAI_ORGANISATION_ID")
  openai.api_key = os.getenv("OPENAI_API_KEY")
  
  response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": prompt}
    ]
  )

  return response["choices"][0]["message"]["content"]

def createEmbedding(text) -> Embedding:
  openai.organization = os.getenv("OPENAI_ORGANISATION_ID")
  openai.api_key = os.getenv("OPENAI_API_KEY")

  dataSet = Embedding()
  dataSet.tokens = getNumberOfTokens(text)

  if dataSet.tokens < MAX_TOKENS:
    response = openai.Embedding.create(
      model=MODEL,
      input=text
    )
    dataSet.vector = np.array(response['data'][0]['embedding'])

    return dataSet
  else:
     print("ERROR: Too many tokens!")
  
def getNumberOfTokens(string):
    encoding = tiktoken.encoding_for_model(MODEL)
    numbersOfToken = len(encoding.encode(string))
    return numbersOfToken 