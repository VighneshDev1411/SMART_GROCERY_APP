catalog = {
    "tomato": {"category": "vegetables", "price": 45},
    "milk": {"category": "dairy", "price": 55},
    "banana": {"category": "fruits", "price": 40},
    "egg": {"category": "poultry", "price": 60},
    "cheese": {"category": "dairy", "price": 120},
}

def enrich_item_metadata(item_name: str):
    return catalog.get(item_name.lower(), {"category":"unknown","price":0 })

