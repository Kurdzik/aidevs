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