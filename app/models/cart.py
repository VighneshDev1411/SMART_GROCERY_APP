from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class UserPreferences(BaseModel):
    dietary_restrictions: List[str] = []
    preferred_stores: List[str] = []
    weekly_budget: Optional[float] = 1000.0

class GroceryItem(BaseModel):
    name: str
    category: str
    price: float = Field(..., gt=0)
    expiry_date: Optional[datetime] = None
    quantity: Optional[str] = "1 unit"

class SmartCartRequest(BaseModel):
    user_id: str
    preferences: UserPreferences
    past_items: List[GroceryItem] = []

class SmartCartResponse(BaseModel):
    suggested_items: List[GroceryItem]
