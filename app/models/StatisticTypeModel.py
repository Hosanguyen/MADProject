from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from app.models.StatisticDataModel import StatisticDataModel

class StatisticTypeModel(BaseModel):
    id: Optional[int] = None  
    name: str
    description: Optional[str] = None
    unit: str
    listStatisticData: List[StatisticDataModel] = Field(default_factory=list)
