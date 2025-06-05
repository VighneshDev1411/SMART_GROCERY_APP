from datetime import datetime
from pymongo import MongoClient
import os

client = MongoClient(os.getenv("MONGO_URI"))
db = client["smart_grocery"]
collection = db["notifications"]

def create_notification(user_id: str, message:str, type_: str = "budget"):
    doc = {
        "user_id": user_id,
        "message": message,
        "type": type_,
        "timestamp": datetime.utcnow()
    }
    collection.insert_one(doc)