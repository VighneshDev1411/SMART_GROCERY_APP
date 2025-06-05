from pydantic import BaseModel
from typing import List, Optional

class EnrichedItem(BaseModel):
    name: str
    confidence: float
    freshness: Optional[str] = "unknown"
    category: Optional[str] = "unknown"
    estimated_price: Optional[float] = 0.0

class EnrichedInventoryResponse(BaseModel):
    items_detected: List[EnrichedItem]
