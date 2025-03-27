from pydantic import BaseModel
from typing import Optional
from app.models.CartItemModel import CartItemModel
from uuid import UUID

class OrderItemModel(BaseModel):
    id: Optional[UUID] = None
    cartItem: CartItemModel
    
