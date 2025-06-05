from pymongo import MongoClient
import os

client = MongoClient(os.getenv("MONGO_URI"))
db = client["smart_grocery"]
collection = db["users"]

def save_user_profile(profile: dict):
    collection.update_one(
        {"user_id": profile["user_id"]},
        {"$set": profile},
        upsert=True
    )

def get_user_profile(user_id: str) -> dict:
    return collection.find_one({"user_id": user_id}) or {}

def get_user_budget(user_id: str) -> float:
    profile = collection.find_one({"user_id": user_id})
    if profile and "weekly_budget" in profile:
        return float(profile["weekly_budget"])
    return 1000.0  # default fallback
