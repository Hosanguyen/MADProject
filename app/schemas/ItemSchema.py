from app.models.ItemModel import ItemModel
from pydantic import BaseModel

class ItemCreate(ItemModel):
    itemTypeId: int

class ItemUpdateQuantity(BaseModel):
    itemId: int
    quantity: int