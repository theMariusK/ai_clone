from database.gridfs_storage import get_file

def stream_video(video_id):
    """Stream video by its ID."""
    file_data = get_file(video_id)
    return file_data  # Properly return a response for video streaming
