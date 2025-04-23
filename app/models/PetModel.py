from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime, date

class PetBase(BaseModel):
    name: str
    # breed_name: str
    # gender: str
    # birth_date: Optional[date] = None
    # color: Optional[str] = None
    # height: float
    # weight: float
    # image_url: Optional[str] = None
    # note: Optional[str] = None
    # userid: Optional[int] = None
    
    # Relationships
    # user: Optional[User] = None
    # vaccinations: List["Vaccination"] = []
    # medical_reports: List["MedicalReport"] = []
    # gps_devices: List["GPSDevice"] = []
    # diary_notes: List["DiaryNote"] = []
    # pet_statistics: List["PetStatistic"] = []
    # pet_reminders: List["PetReminder"] = []
    
    
class PetCreate(PetBase):
    id: Optional[str] = None
    breed_name: str
    gender: str
    birth_date: Optional[date] = None
    color: Optional[str] = None
    height: float
    weight: float
    image_url: Optional[str] = None
    userid: str

class PetResponse(BaseModel):
    id: str