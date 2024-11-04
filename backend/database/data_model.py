# database/data_model.py

from mongoengine import Document, StringField, FileField, DictField

class Video(Document):
    title = StringField(required=True)
    description = StringField()
    file = FileField()  # For storing video files

class Audio(Document):
    title = StringField(required=True)
    description = StringField()
    file = FileField()  # For storing audio files

class Metadata(Document):
    title = StringField(required=True)
    data = DictField()  # For storing metadata in JSON format
