from datetime import datetime, timedelta

def get_fridge_items(user_id: str) -> list[dict]:
    # This would normally hit MongoDB
    return [
        {
            "name": "Spinach",
            "expiry_date": "2025-06-06"
        },
        {
            "name": "Milk",
            "expiry_date": "2025-06-05"
        },
        {
            "name": "Rice",
            "expiry_date": None
        }
    ]
