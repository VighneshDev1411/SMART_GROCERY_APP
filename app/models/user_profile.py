from pydantic import BaseModel
from typing import List, Optional

class UserProfile(BaseModel):
    user_id: str
    dietary_restrictions: List[str] = []
    preferred_stores: List[str] = []
    weekly_budget: Optional[float] = 1000.0

