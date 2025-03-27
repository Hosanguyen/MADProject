from pydantic import BaseModel
from typing import Optional
from app.models.ItemModel import ItemModel
from uuid import UUID

class CartItemModel(BaseModel):
    id: Optional[UUID] = None
    quantity: int
    item: ItemModel
    
