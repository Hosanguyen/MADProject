from pydantic import BaseModel
from typing import Optional
from app.models.ItemModel import ItemModel

class CartItemModel(BaseModel):
    id: Optional[int] = None
    quantity: int
    item: ItemModel
    
