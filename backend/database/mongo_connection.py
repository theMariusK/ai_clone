# backend/database/mongo_connection.py
from pymongo import MongoClient
import gridfs
import os

client = MongoClient(os.getenv("MONGO_URI"))
db = client["media_db"]
fs = gridfs.GridFS(db)

def initialize_db():
    print("Database initialized")
