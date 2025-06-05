from app.db.product_catalog import enrich_item_metadata

def score_freshness(item_name:str) -> str:
    freshness_map = {
        "banana": "overripe",
        "tomato": "good",
        "milk": "good",
        "egg": "good",
        "cheese": "moderate"
    }

    return freshness_map.get(item_name.lower(), "unknown")

def postprocess_vision_output(raw_detections: list, confidence_threshold: float=0.6):
    enriched = []
    for item in raw_detections:
        if item["confidence"] < confidence_threshold:
            continue
        
        meta = enrich_item_metadata(item["name"])
        enriched.append({
            "name": item["name"],
            "confidence": item["confidence"],
            "freshness": score_freshness(item["name"]),
            "category": meta["category"],
            "estimated_price": meta["price"]
        })

        return enriched