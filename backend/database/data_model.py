class FileMetadataModel:
    def __init__(self, file_path, content_type):
        self.file_path = file_path
        self.content_type = content_type

    def to_dict(self):
        return {
            "path": self.file_path,
            "content_type": self.content_type,
        }