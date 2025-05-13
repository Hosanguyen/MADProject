from pydantic import BaseModel, Field
from uuid import UUID
from typing import List, Optional
from app.models.OrderItemModel import OrderItemModel
class OrderCreate(BaseModel):
    id: Optional[UUID] = None
    userId: UUID

class OrderInit(BaseModel):
    id: Optional[UUID] = None
    userId: UUID
    listItem: List[OrderItemModel] = Field(default_factory=list)