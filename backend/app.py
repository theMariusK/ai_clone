from flask import Flask, request, jsonify
from api_gateway.config import API_VERSION
from services.data_processing_service import process_video, process_audio
from services.streaming_service import stream_video
from database.gridfs_storage import store_video, store_audio
from database.data_model import Video, Audio, Metadata

app = Flask(__name__)

@app.route(f"/{API_VERSION}/upload_video", methods=["POST"])
def upload_video():
    video_file = request.files['file']
    title = request.form.get('title')
    description = request.form.get('description')

    video_id = store_video(video_file, title)
    video = Video(title=title, description=description, file=video_id)
    video.save()

    return jsonify({"message": "Video uploaded successfully", "video_id": str(video.id)}), 201

@app.route(f"/{API_VERSION}/upload_audio", methods=["POST"])
def upload_audio():
    audio_file = request.files['file']
    title = request.form.get('title')
    description = request.form.get('description')

    audio_id = store_audio(audio_file, title)
    audio = Audio(title=title, description=description, file=audio_id)
    audio.save()

    return jsonify({"message": "Audio uploaded successfully", "audio_id": str(audio.id)}), 201

@app.route(f"/{API_VERSION}/stream_video/<video_id>", methods=["GET"])
def stream_video_route(video_id):
    return stream_video(video_id)


@app.route(f"/{API_VERSION}/test", methods=["GET"])
def test_route():
    return jsonify({"message": "Test route is working"}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
