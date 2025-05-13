from pydantic import BaseModel, Field
from typing import Optional, List
from app.models.OrderItemModel import OrderItemModel
from app.models.User import UserBase
from uuid import UUID

from app.schemas.OrderItemSchema import OrderItemResponse

class OrderModel(BaseModel):
    id: Optional[UUID] = None
    listOrderItem: List[OrderItemResponse] = Field(default_factory=list)
    user: UserBase = Field(default_factory=None)
