from pydantic import BaseModel
from typing import Optional
from app.schemas.ItemSchema import ItemResponseCart
from uuid import UUID
from datetime import datetime
class CartItemModel(BaseModel):
    id: Optional[UUID] = None
    quantity: int
    item: Optional[ItemResponseCart] = None