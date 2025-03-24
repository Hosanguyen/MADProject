from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class StatisticDataModel(BaseModel):
    id: Optional[int] = None
    statisticTypeId: int
    value: float
    timestamp: datetime = datetime.utcnow()
