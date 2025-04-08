from app.models.ItemModel import ItemModel
from pydantic import BaseModel
from uuid import UUID
from typing import Optional
class ItemCreate(ItemModel):
    itemTypeId: UUID

class ItemUpdateQuantity(BaseModel):
    itemId: UUID
    quantity: int

class ItemResponseCart(BaseModel):
    id: UUID
    name: str
    price: float
    description: Optional[str] = None
    manufacturer: str
    