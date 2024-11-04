# backend/services/streaming_service.py
from database.mongo_connection import fs
from flask import Response, jsonify

def stream_video(video_id):
    try:
        file = fs.get(video_id)
        return Response(file, content_type='video/mp4')
    except Exception:
        return jsonify({'error': 'Video not found'}), 404