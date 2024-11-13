# some_other_module.py
import os
from database.connection import db
from bson.objectid import ObjectId
from werkzeug.utils import secure_filename

not_processed_folder = os.getenv("NOT_PROCESSED_FOLDER")
video_folder = os.getenv("VIDEO_FOLDER")
audio_folder = os.getenv("AUDIO_FOLDER")

def _initialize_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)

def initialize_storage():
    _initialize_folder(os.getenv("UPLOAD_FOLDER"))
    _initialize_folder(not_processed_folder)
    _initialize_folder(video_folder)
    _initialize_folder(audio_folder)

    print("Folders initialized successfully")

def store_video(video_file, title, description):
    # Save video to local storage
    filename = secure_filename(video_file.filename)
    video_path = os.path.join(not_processed_folder, filename)
    video_file.save(video_path)
    
    # Store metadata in MongoDB
    video_metadata = {
        "title": title,
        "description": description,
        "path": video_path,
        "content_type": video_file.content_type,
    }
    
    result = db.files.insert_one(video_metadata)
    return str(result.inserted_id)



# Common

def get_file(video_id):
    video_metadata = db.files.find_one({"_id": ObjectId(video_id)})
    if not video_metadata:
        return None
    
    video_path = video_metadata.get("path")
    if not video_path or not os.path.exists(video_path):
        return None
    
    with open(video_path, "rb") as video_file:
        video_content = video_file.read()
    
    return {
        "title": video_metadata.get("title"),
        "description": video_metadata.get("description"),
        "content_type": video_metadata.get("content_type"),
        # "content": video_content
    }

def delete_file(file_id):
    file_metadata = db.files.find_one({"_id": ObjectId(file_id)})
    if not file_metadata:
        print("File not found")
        return False
    
    file_path = file_metadata.get("path")
    if not file_path or not os.path.exists(file_path):
        print("File path not found")
        return False

    os.remove(file_path)
    db.files.delete_one({"_id": ObjectId(file_id)})
    
    # Clean up other linked metadata to certain file
    db.files.delete_many({"path": file_path})
    
    return True


