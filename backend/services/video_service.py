import os
from config import VIDEO_STORAGE_PATH

# Function to store video in local storage
def store_video_locally(file, filename):
    file_path = os.path.join(VIDEO_STORAGE_PATH, filename)
    file.save(file_path)
