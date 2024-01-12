from flask import Flask, jsonify, request
from flask_cors import CORS

import api_handler

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})

# A simple in-memory storage for chat history
chat_history = []

@app.route('/ping', methods=['POST'])
def ping_pong():
    data = {"response": "pong!"}
    return jsonify(data)

@app.route('/chat', methods=['POST'])
def chat():
    if request.method == 'POST':
        data = request.get_json()
        message = data.get('message', '')
        incoming_chat_history = data.get('chat_history', [])

        # Update the global chat_history with incoming_chat_history
        global chat_history
        chat_history = chat_history + incoming_chat_history

        print(chat_history)
        # Process the message and get a response
        response = api_handler.call_openai(message,chat_history)


        # Update the chat history with the user's message and the bot's response
        chat_history.append({'sender': 'Human', 'content': message})
        chat_history.append({'sender': 'AI', 'content': response})

        # Return the response and the updated chat history
        return jsonify({'response': response, 'updatedChatHistory': chat_history})


if __name__ == '__main__':
    app.run(port=5000)