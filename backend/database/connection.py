from pymongo import MongoClient
import os

# Set up MongoDB connection and GridFS
client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("DB_NAME")]