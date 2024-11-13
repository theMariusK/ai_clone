from pymongo import MongoClient

class FileMetadataModel:
    def __init__(self, title, description, file_path, content_type):
        self.title = title
        self.description = description
        self.file_path = file_path
        self.content_type = content_type

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "path": self.file_path,
            "content_type": self.content_type,
        }