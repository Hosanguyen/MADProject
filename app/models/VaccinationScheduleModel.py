from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime, date, time

class VaccinationScheduleModel(BaseModel):
    schedule_id: Optional[UUID] = None
    pet_id: UUID
    vaccine_type: str
    vaccination_date: date
    vaccination_time: time
    clinic_name: Optional[str] = None
    status: str = 'Pending'
    reminder_before_days: Optional[int] = None
    reminder_before_hours: Optional[int] = None
    created_at: datetime
    updated_at: datetime