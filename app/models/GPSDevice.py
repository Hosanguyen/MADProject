from pydantic import BaseModel
from typing import Optional
from datetime import datetime
    
class GPSDevice(BaseModel):
    id: str
    name: Optional[str]
    latitude: float = -1.0
    longitude: float = -1.0
    status: Optional[str] = "Connected"
    battery: int = -1
    image_url: Optional[str] = None
    petid: Optional[str]