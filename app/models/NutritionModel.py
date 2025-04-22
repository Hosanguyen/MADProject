from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class NutritionInfoModel(BaseModel):
    id: Optional[UUID] = None
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    pet_type: Optional[str] = None
    created_at: datetime
    updated_at: datetime
