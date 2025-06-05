from pydantic import BaseModel
from typing import List

class DetectedItem(BaseModel):
    name: str
    confidence: float

class VisionResponse(BaseModel):
    items_detected: List[DetectedItem]
