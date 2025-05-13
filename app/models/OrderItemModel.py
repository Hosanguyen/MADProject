from pydantic import BaseModel
from typing import Optional
from app.models.CartItemModel import CartItemModel
from uuid import UUID
from app.schemas.CartItemSchema import CartItemOrder
class OrderItemModel(BaseModel):
    id: Optional[UUID] = None
    cartItem: CartItemOrder
    
