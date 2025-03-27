from pydantic import BaseModel
from typing import Optional
import uuid

class ItemModel(BaseModel):
    id: Optional[uuid.UUID] = None
    name: str
    quantity: int
    price: float
    description: Optional[str] = None
    manufacturer: str
    