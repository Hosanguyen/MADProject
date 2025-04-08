from app.models.OrderItemModel import OrderItemModel
from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class OrderItemCreate(BaseModel):
    id: Optional[UUID] = None
    orderId: UUID
    cartItemId: UUID
