from pydantic import BaseModel, Field
from typing import Optional, List
from app.models.OrderItemModel import OrderItemModel
# from app.models.UserModel import UserModel
from uuid import UUID

class OrderModel(BaseModel):
    id: Optional[UUID] = None
    listOrderItem: List[OrderItemModel] = Field(default_factory=list)
    # user: UserModel
