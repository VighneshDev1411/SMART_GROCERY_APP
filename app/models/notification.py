from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Notification(BaseModel):
    user_id: str
    message: str
    type: str
    timestamp: Optional[datetime] = datetime.utcnow()