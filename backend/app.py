import uuid
from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify
from flask_socketio import SocketIO
import requests
import eventlet
import eventlet.wsgi
from config import not_processed_folder, video_folder, audio_folder, initialize_storage, API_VERSION
from database.storage import store_file, get_file, delete_file, store_file_metadata, store_audio_processing_metadata, store_video_processing_metadata
from internal_modules.data_processing_module import separate_video_audio, process_video, process_audio
from internal_modules.replication_module import conversation_input

app = Flask(__name__)
socketio = SocketIO(app)



# Web socket manager

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('message')
def handle_message(data):
    print(f"Received message: {data}")
    socketio.emit('response', f"Server says: {data}")
    


# Replication routes

@app.route(f"/{API_VERSION}/conversation-input", methods=['POST'])
def conversation_input_route():
    print(request.json)
    
    assistant_output = conversation_input(request.json.get("value"))
    if assistant_output is None:
        return jsonify({"message": "Error sending data to language model"}), 500
    print(assistant_output)
    
    socketio.emit('conversation_input', assistant_output)
    
    return jsonify({"message": "Replication service called successfully"}), 200



# Video routes

@app.route(f"/{API_VERSION}/process", methods=['POST'])
def process_video_route():
    print("process_video")
    
    process_uid = str(uuid.uuid4())
    non_processed_file = request.files['file']
    
    non_processed_result = store_file(
        secure_filename(non_processed_file.filename),
        non_processed_file.read(),
        not_processed_folder,
        non_processed_file.content_type,
        process_uid
    )
    if not non_processed_result:
        return jsonify({"message": "Error processing video"}), 500
    
    metadata = get_file(non_processed_result)
    if not metadata:
        return jsonify({"message": "Error retrieving file metadata"}), 500
    
    path = metadata.get("path")
    if not path:
        return jsonify({"message": "Error retrieving file path"}), 500
    
    video, audio = separate_video_audio(path, video_folder, audio_folder)
    if not video or not audio:
        return jsonify({"message": "Error separating video and audio"}), 500
    
    video_result = store_file_metadata(process_uid, video, f"video{process_uid}")
    audio_result = store_file_metadata(process_uid, audio, f"audio{process_uid}")
    if not video_result or not audio_result:
        return jsonify({"message": "Error storing video and audio metadata"}), 500
        
    # Delete the non-processed file
    delete_file(non_processed_result)
    
    # Process the video and audio
    video_processed_result = process_video(video, audio)
    if 'error' in video_processed_result:
        return jsonify({"message": f"Error processing video, {video_processed_result.get('error')}"}), 500
    audio_processed_result = process_audio(audio)
    
    # Store the results of processing
    store_video_processing_metadata(process_uid, video_processed_result)
    store_audio_processing_metadata(process_uid, audio_processed_result)
    
    # Delete the video and audio files
    delete_file(video_result)
    delete_file(audio_result)

    return jsonify({"message": "Video processed and stored successfully", "process_uid": str(process_uid)})



# Common routes

@app.route(f"/{API_VERSION}/<file_id>", methods=['DELETE'])
def delete_file_route(file_id):
    result = delete_file(file_id)
    if result:
        return jsonify({"message": "File deleted successfully"}), 200
    else:
        return jsonify({"message": "File not found"}), 404

@app.route(f"/{API_VERSION}/test", methods=["GET"])
def test_route():
    print("test")
    return jsonify({"message": "Test route is working"}), 200

@app.route(f"/{API_VERSION}/replication/test_socket", methods=["GET"])
def test_socket_route():
    print("test_socket")
    socketio.emit('test', "Test socket message")
    return jsonify({"message": "Test socket route is working"}), 200



# Run
 
if __name__ == "__main__":
    initialize_storage()
    socketio.run(app, host="0.0.0.0", port=5000)
