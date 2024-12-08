from flask import Flask, request, jsonify
from ..config import API_VERSION, LANGUAGE_MODEL_URL
import time

app = Flask(__name__)

@app.route(f"/{API_VERSION}/replication/conversation_input", methods=["POST"])
def conversation_input_route():
    print("conversation_input")
    
    # Send data to language model
    data = request.json
    response = request.post(f"{LANGUAGE_MODEL_URL}/{API_VERSION}/replication/language_model_placeholder", json=data)
    if response.status_code != 200:
        return jsonify({"message": "Error sending data to language model"}), 500
    conversation_output = response.json()
    
    # Send conversation_output to text-to-speech service
    tts_response = request.post(f"{LANGUAGE_MODEL_URL}/{API_VERSION}/replication/text_to_speech_placeholder", json=conversation_output)
    if tts_response.status_code != 200:
        return jsonify({"message": "Error generating audio from text"}), 500
    audio_output = tts_response.json()
    
    # Send audio_output to client
    socketio.emit('conversation_input', audio_output)
    return jsonify({"message": "Conversation input sent successfully"}), 200

@app.route(f"/{API_VERSION}/replication/language_model_placeholder", methods=["POST"])
def language_model_placeholder_route():
    print("language_model_placeholder")
    time.sleep(15)
    return jsonify({"message": "AI placeholder sent successfully"}), 200

@app.route(f"/{API_VERSION}/replication/text_to_speech_placeholder", methods=["POST"])
def text_to_speech_placeholder_route():
    print("text_to_speech_placeholder")
    time.sleep(15)
    return jsonify({"message": "Text-to-speech placeholder sent successfully"}), 200

if __name__ == "__main__":
    app.run(app, host="0.0.0.0", port=5002)
