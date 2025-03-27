from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from app.models.StatisticDataModel import StatisticDataModel
from uuid import UUID

class StatisticTypeModel(BaseModel):
    id: Optional[UUID] = None  
    name: str
    description: Optional[str] = None
    unit: str
    listStatisticData: List[StatisticDataModel] = Field(default_factory=list)
