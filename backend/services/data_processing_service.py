# backend/services/data_processing_service.py
from database.mongo_connection import fs
from flask import jsonify

def process_data(file):
    if file:
        file_id = fs.put(file, filename=file.filename)
        return jsonify({'message': 'File processed and stored.', 'file_id': str(file_id)}), 201
    return jsonify({'error': 'No file provided'}), 400