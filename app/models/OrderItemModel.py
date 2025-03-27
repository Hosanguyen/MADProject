from pydantic import BaseModel
from typing import Optional
from app.models.CartItemModel import CartItemModel

class OrderItemModel(BaseModel):
    id: Optional[int] = None
    cartItem: CartItemModel
    
