from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class StatisticTypeModel(BaseModel):
    id: Optional[int] = None  
    name: str
    description: Optional[str] = None
    unit: str
