import requests
import os
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

APIKEY = os.getenv('APIKEY')
OPENAI_APIKEY = os.getenv('OPENAI_APIKEY')

class Question:
    def __init__(self,task):
        self.task = task

    @staticmethod
    def _get_question_token(task_name):
        url = f"https://zadania.aidevs.pl/token/{task_name}"
        headres = {"apikey": APIKEY}
        response = requests.post(url=url, json=headres).json()

        return response["token"]

    @staticmethod
    def _get_question(token):
        url = f"https://zadania.aidevs.pl/task/{token}"
        response = requests.get(url=url).json()

        return response

    def get(self):
        token = self._get_question_token(self.task)
        question = self._get_question(token)

        return question

class Answer:
    def __init__(self,task):
        self.task = task

    @staticmethod
    def _get_question_token(task_name):
        url = f"https://zadania.aidevs.pl/token/{task_name}"
        headres = {"apikey": APIKEY}
        response = requests.post(url=url, json=headres).json()

        return response["token"]
    
    @staticmethod
    def _send_answer(answer,token):
        url = f"https://zadania.aidevs.pl/answer/{token}"
        headres = {"answer": answer}
        response = requests.post(url=url, json=headres).json()

        return response
    
    def post(self,answer):
        token = self._get_question_token(self.task)
        response = self._send_answer(answer,token)

        return response

class QA:
    def __init__(self,task):
        self.task = task
        self.token = self._get_question_token(self.task)

    @staticmethod
    def _get_question_token(task_name):
        url = f"https://zadania.aidevs.pl/token/{task_name}"
        headres = {"apikey": APIKEY}
        response = requests.post(url=url, json=headres).json()

        return response["token"]

    def _get_question(self):
        url = f"https://zadania.aidevs.pl/task/{self.token}"
        response = requests.get(url=url).json()

        return response

    def get(self):
        question = self._get_question()

        return question
    
    def _send_answer(self,answer):
        url = f"https://zadania.aidevs.pl/answer/{self.token}"
        headres = {"answer": answer}
        response = requests.post(url=url, json=headres).json()

        return response
    
    def post(self,answer):
        response = self._send_answer(answer)

        return response


def create_embeddings(text):
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_APIKEY)
    
    return embeddings.embed_query(text)

def create_transcript(mp3_path):

    client = OpenAI(api_key=OPENAI_APIKEY)


    audio_file= open(mp3_path, "rb")
    transcript = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file,
    response_format="text",
    
    )

    return transcript

def llm_predict(prompt):
    llm = ChatOpenAI(openai_api_key=OPENAI_APIKEY,
                    model="gpt-3.5-turbo",
                    streaming=False)
    return llm.predict(prompt)

from tenacity import retry,wait_exponential,retry_if_exception_type
import requests
import json,random

class CustomException(Exception):
    pass

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'
]


headers = {'User-Agent': random.choice(user_agents)}

@retry(retry=retry_if_exception_type(CustomException)| wait_exponential(multiplier=1, min=4, max=10))
def get_text(url,output_file):
    request = requests.get(url,headers=headers,timeout=0)
    if request.text in ['server error X_X']:
        raise CustomException
    
    with open(output_file,"w+") as file:
        file.write(request.text)