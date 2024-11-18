import uuid
from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify
from config import not_processed_folder, video_folder, audio_folder, initialize_storage
from api_gateway.config import API_VERSION
from database.storage import store_file, get_file, delete_file, store_file_metadata
from services.data_processing_service import separate_video_audio, process_video, process_audio

app = Flask(__name__)



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
    delete_file(non_processed_result);
    
    # Process the video and audio
    video_processed_result = process_video(video)
    audio_processed_result = process_audio(audio)
    
    # Store the results of processing
    # Fill the code here
    
    # Delete the video and audio files
    delete_file(video_result)
    delete_file(audio_result)

    return jsonify({"message": "Video processed and stored successfully", "process_uid": str(process_uid)})

@app.route(f"/{API_VERSION}/video", methods=['POST'])
def upload_video_route():
    print("upload_video")
    
    video_file = request.files['file']
    
    result = store_file(video_file)

    return jsonify({"message": "Video uploaded successfully", "video_id": str(result)})

@app.route(f"/{API_VERSION}/video/<video_id>", methods=['GET'])
def get_video_route(video_id):
    video_data = get_file(video_id)
    if video_data:
        return jsonify({"video_id": video_id, "video_data": video_data}), 200
    else:
        return jsonify({"message": "Video not found"}), 404



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



# Run
 
if __name__ == "__main__":
    initialize_storage()
    app.run(host='0.0.0.0', port=5000)
