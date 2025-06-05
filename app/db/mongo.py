from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client["smart_grocery"]
users_collection = db["users"]
cart_collection = db["cart_history"]
products_collection = db["products"]
