from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class StatisticDataModel(BaseModel):
    id: Optional[UUID] = None
    value: float
    recorded_at: datetime = datetime.utcnow()
