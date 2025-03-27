from app.models.ItemModel import ItemModel
from pydantic import BaseModel
from uuid import UUID

class ItemCreate(ItemModel):
    itemTypeId: UUID

class ItemUpdateQuantity(BaseModel):
    itemId: UUID
    quantity: UUID