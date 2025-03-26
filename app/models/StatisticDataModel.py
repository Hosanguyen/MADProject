from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class StatisticDataModel(BaseModel):
    id: Optional[int] = None
    value: float
    recorded_at: datetime = datetime.utcnow()
