# backend/api_gateway/gateway.py
from flask import Blueprint, request
from services.data_processing_service import process_data
# from services.streaming_service import stream_video

api_gateway = Blueprint('api_gateway', __name__)

@api_gateway.route('/process', methods=['POST'])
def data_processing():
    # Call Data Processing Service
    data = request.files.get('file')
    return process_data(data)

# @api_gateway.route('/stream/<video_id>', methods=['GET'])
# def video_streaming(video_id):
#     # Call Streaming Service
#     return stream_video(video_id)