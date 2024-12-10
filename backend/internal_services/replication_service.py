from flask import request, jsonify
import requests
from config import LANGUAGE_MODEL_ENDPOINT

headers = {
    "Content-Type": "application/json"
}

history = []

def conversation_input(user_message):
    print("conversation_input")
    history.append({"role": "user", "content": user_message})
    data = {
        "mode": "chat",
        "character": "Example",
        "messages": history
    }
    
    response = requests.post(f"{LANGUAGE_MODEL_ENDPOINT}/v1/chat/completions", headers=headers, json=data, verify=False)
    if response.status_code != 200:
        print(f"{response.status_code}: Failed to get response from language model")
        return None
    assistant_message = response.json()['choices'][0]['message']['content']
    history.append({"role": "assistant", "content": assistant_message})
    
    return assistant_message
