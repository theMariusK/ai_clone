class FileMetadataModel:
    def __init__(self, process_uid, file_path, content_type):
        self.process_uid: str = process_uid
        self.file_path: str = file_path
        self.content_type: str = content_type

    def to_dict(self):
        return {
            "process_uid": self.process_uid,
            "path": self.file_path,
            "content_type": self.content_type,
        }
    
class AudioProcessingMetadataModel:
    def __init__(self, process_uid, spectogram):
        self.process_uid = process_uid
        self.spectogram = spectogram
    
    def to_dict(self):
        return {
            "process_uid": self.process_uid,
            "spectogram": self.spectogram
        }

class VideoProcessingMetadataModel:
    def __init__(self, process_uid, processing_details):
        self.process_uid = process_uid
        self.processing_details = processing_details  # dictionary of processing details
    
    def to_dict(self):
        return {
            "process_uid": self.process_uid,
            "processing_details": self.processing_details
        }
