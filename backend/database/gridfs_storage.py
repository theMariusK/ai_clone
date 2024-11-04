# database/gridfs_storage.py

import gridfs
from pymongo import MongoClient

# Set up MongoDB connection
client = MongoClient('mongodb://mongo:27017/')
db = client['your_database_name']
fs = gridfs.GridFS(db)

def store_video(file_data, filename):
    """Store a video file in GridFS."""
    return fs.put(file_data, filename=filename)

def store_audio(file_data, filename):
    """Store an audio file in GridFS."""
    return fs.put(file_data, filename=filename)

def get_file(file_id):
    """Retrieve a file from GridFS by its ID."""
    return fs.get(file_id).read()

def delete_file(file_id):
    """Delete a file from GridFS by its ID."""
    fs.delete(file_id)
