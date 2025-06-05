from pydantic import BaseModel
from typing import List

class ReceiptItem(BaseModel):
    name: str
    price: float

class ReceiptResponse(BaseModel):
    store: str
    date: str  # Consider converting to datetime in next phase
    items: List[ReceiptItem]
    total: float

