# app/memory/receipt_memory.py

from typing import List, Dict

# In-memory store
receipt_memory: List[Dict] = []

def store_receipt(user_id: str, receipt_data: dict):
    entry = {
        "user_id": user_id,
        "receipt": receipt_data
    }
    receipt_memory.append(entry)

def get_all_receipts(user_id: str):
    return [
        entry["receipt"] for entry in receipt_memory
        if entry.get("user_id") == user_id
    ]
