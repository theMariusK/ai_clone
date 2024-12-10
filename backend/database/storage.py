import os
from database.connection import db
from bson.objectid import ObjectId
from database.data_model import FileMetadataModel, AudioProcessingMetadataModel,VideoProcessingMetadataModel


def store_file(filename: str, file_content: bytes, folder: str, content_type: str, process_uid: str) -> str:
    # Save file to local storage
    file_path = os.path.join(folder, filename)
    with open(file_path, 'wb') as f:
        f.write(file_content)
    
    # Store metadata in MongoDB using FileMetadataModel
    result = store_file_metadata(process_uid, file_path, content_type)
    return str(result)


# Audio results

# Function to store audio processing metadata without file_path and content_type
def store_audio_processing_metadata(process_uid: str, processing_details) -> str:
    # Creating metadata for the audio processing without file_path and content_type
    audio_metadata = AudioProcessingMetadataModel(process_uid, processing_details)
    result = db.audio_processing_metadata.insert_one(audio_metadata.to_dict())  # Storing audio processing metadata
    return str(result.inserted_id)


# Modify metadata of existing audio processing data
def modify_audio_processing_metadata(metadata_id: str, new_metadata: dict):
    audio_metadata = db.audio_processing_metadata.find_one({"_id": ObjectId(metadata_id)})
    if not audio_metadata:
        print("Metadata not found")
        return False
    
    db.audio_processing_metadata.update_one({"_id": ObjectId(metadata_id)}, {"$set": new_metadata})

# Retrieve audio processing metadata by its ID
def get_audio_processing_metadata(metadata_id: str):
    audio_metadata = db.audio_processing_metadata.find_one({"_id": ObjectId(metadata_id)})
    if not audio_metadata:
        print("Metadata not found")
        return None
    
    return audio_metadata

# Delete audio processing metadata
def delete_audio_processing_metadata(metadata_id: str):
    audio_metadata = db.audio_processing_metadata.find_one({"_id": ObjectId(metadata_id)})
    if not audio_metadata:
        print("Metadata not found")
        return False
    
    # Clean up any additional metadata if needed
    db.audio_processing_metadata.delete_one({"_id": ObjectId(metadata_id)})
    
    return True

# video result 
 # Function to store video processing metadata
def store_video_processing_metadata(process_uid: str, processing_details: dict) -> str:
    # Create metadata for video processing
    video_metadata = VideoProcessingMetadataModel(
        process_uid=process_uid,
        processing_details=processing_details  # Details like video format, processing steps, etc.
    )
    result = db.video_processing_metadata.insert_one(video_metadata.to_dict())  # Store video processing metadata
    return str(result.inserted_id)

# Modify metadata of existing video processing data
def modify_video_processing_metadata(metadata_id: str, new_metadata: dict):
    video_metadata = db.video_processing_metadata.find_one({"_id": ObjectId(metadata_id)})
    if not video_metadata:
        print("Metadata not found")
        return False
    
    db.video_processing_metadata.update_one({"_id": ObjectId(metadata_id)}, {"$set": new_metadata})

# Retrieve video processing metadata by its ID
def get_video_processing_metadata(metadata_id: str):
    video_metadata = db.video_processing_metadata.find_one({"_id": ObjectId(metadata_id)})
    if not video_metadata:
        print("Metadata not found")
        return None
    
    return video_metadata

# Delete video processing metadata
def delete_video_processing_metadata(metadata_id: str):
    video_metadata = db.video_processing_metadata.find_one({"_id": ObjectId(metadata_id)})
    if not video_metadata:
        print("Metadata not found")
        return False
    
    # Clean up any additional metadata if needed
    db.video_processing_metadata.delete_one({"_id": ObjectId(metadata_id)})
    
    return True
# Common

def modify_file_metadata(file_id, new_metadata):
    file_metadata = db.files.find_one({"_id": ObjectId(file_id)})
    if not file_metadata:
        print("File not found")
        return False
    
    db.files.update_one({"_id": ObjectId(file_id)}, {"$set": new_metadata })

def store_file_metadata(process_uid: str, file_path: str, content_type: str) -> str:
    file_metadata = FileMetadataModel(process_uid, file_path, content_type)
    result = db.files.insert_one(file_metadata.to_dict())
    return str(result.inserted_id)

def get_file(file_id):
    file_metadata = db.files.find_one({"_id": ObjectId(file_id)})
    if not file_metadata:
        print("File not found")
        return None
    
    return file_metadata

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


