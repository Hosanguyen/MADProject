from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class ItemModel(BaseModel):
    id: Optional[UUID] = None
    name: str
    quantity: int
    price: float
    description: Optional[str] = None
    manufacturer: str
    image_url: Optional[str] = None