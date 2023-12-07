# python
from flask import Flask
from flask import request
import os,json
from langchain.chat_models import ChatOpenAI
from langchain.schema.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv
load_dotenv('../.env')

OPENAI_APIKEY= os.getenv('OPENAI_APIKEY')

messages = [SystemMessage(content="Hi")]
chat = ChatOpenAI(api_key=OPENAI_APIKEY,streaming=False)

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the home page!"

@app.route('/chat', methods=['GET', 'POST'])
def answer():
    if request.method == 'POST':
        data = request.get_json()
        
        question = data.get('question', None)
        print("======================")
        print("Question:",question)
        print("======================")

        human_message = HumanMessage(content=question)
        messages.append(human_message)

        ai_message = chat.invoke(messages)
        messages.append(ai_message)

        reponse = json.dumps({'reply': ai_message.content})

        return reponse

    else:
        return "This is the answer page!"

if __name__ == '__main__':
    app.run(debug=True,
            host='0.0.0.0',
            port=5001)
