from pymongo import MongoClient
import os

client = MongoClient(os.getenv("MONGO_URI"))
db = client["smart_grocery"]
collection = db["notifications"]

from bson import ObjectId

def get_user_alerts(user_id: str) -> list[dict]:
    results = collection.find({"user_id": user_id}).sort("timestamp", -1)
    alerts = []

    for alert in results:
        alert["_id"] = str(alert["_id"])  # Convert ObjectId to string
        alerts.append(alert)

    return alerts
