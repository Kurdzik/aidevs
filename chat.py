from langchain.chat_models.openai import ChatOpenAI
from langchain.schema.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv
import os

load_dotenv('.env')
OPENAI_APIKEY = os.getenv('OPENAI_APIKEY')

chat = ChatOpenAI(api_key=OPENAI_APIKEY)

messages = [SystemMessage(content="Hi")]

while True:
    message = input('USER: ')
    human_message = HumanMessage(content=message)
    messages.append(human_message)

    ai_message = chat.invoke(messages)
    print('AI:',ai_message.content)
    messages.append(ai_message)
