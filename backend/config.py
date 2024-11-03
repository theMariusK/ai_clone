import os

# MongoDB connection URI
MONGODB_URI = 'mongodb://localhost:27017/'

# Directory to store videos
VIDEO_STORAGE_PATH = './storage/videos/'
if not os.path.exists(VIDEO_STORAGE_PATH):
    os.makedirs(VIDEO_STORAGE_PATH)
