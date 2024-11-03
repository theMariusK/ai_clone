from pymongo import MongoClient
import gridfs
from config import MONGODB_URI

# Connect to MongoDB and get the database and GridFS
client = MongoClient(MONGODB_URI)
db = client['media_storage']
fs = gridfs.GridFS(db)

# Function to store image in MongoDB
def store_image_in_mongodb(file, filename):
    fs.put(file, filename=filename)
