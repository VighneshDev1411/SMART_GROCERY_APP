from app.db.mongo import cart_collection
from app.models.cart import SmartCartRequest, GroceryItem
from datetime import datetime

def save_cart(user_id: str, items: list[GroceryItem]):
    cart_doc = {
        "user_id": user_id,
        "items": [item.dict() for item in items],
        "timestamp": datetime.utcnow()
    }
    cart_collection.insert_one(cart_doc)

def get_user_cart_history(user_id: str, limit=5):
    return list(cart_collection.find({"user_id": user_id}).sort("timestamp", -1).limit(limit))
