from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class DiseaseModel(BaseModel):
    id: Optional[UUID] = None
    name: str
    description: Optional[str] = None
    symptoms: Optional[str] = None
    treatment: Optional[str] = None
    prevention: Optional[str] = None
    pet_type: Optional[str] = None
    severity: Optional[str] = None
    created_at: datetime
    updated_at: datetime