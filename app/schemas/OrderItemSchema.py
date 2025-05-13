from app.models.CartItemModel import CartItemModel
from app.models.OrderItemModel import OrderItemModel
from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class OrderItemCreate(BaseModel):
    id: Optional[UUID] = None
    orderId: UUID
    cartItemId: UUID

class OrderItemResponse(BaseModel):
    id: Optional[UUID] = None
    cartItem: CartItemModel