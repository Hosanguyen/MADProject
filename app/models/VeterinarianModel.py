from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class VeterinarianModel(BaseModel):
    id: Optional[UUID] = None
    name: str
    specialization: Optional[str] = None
    years_of_experience: Optional[int] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    rating: Optional[float] = None
    clinic_name: Optional[str] = None
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime