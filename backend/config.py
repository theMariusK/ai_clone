import os

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
