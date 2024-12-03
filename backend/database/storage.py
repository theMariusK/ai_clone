import os
from database.connection import db
from bson.objectid import ObjectId
from database.data_model import FileMetadataModel


def store_file(filename: str, file_content: bytes, folder: str, content_type: str, process_uid: str) -> str:
    # Save file to local storage
    file_path = os.path.join(folder, filename)
    with open(file_path, 'wb') as f:
        f.write(file_content)
    
    # Store metadata in MongoDB using FileMetadataModel
    result = store_file_metadata(process_uid, file_path, content_type)
    return str(result)


def Fuck():

    pass


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


