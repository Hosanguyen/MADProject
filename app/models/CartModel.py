from pydantic import BaseModel, Field
from typing import Optional, List
from app.models.CartItemModel import CartItemModel
from uuid import UUID

class CartModel(BaseModel):
    id: Optional[UUID] = None
    userId: UUID
    listItem: List[CartItemModel] = Field(default_factory=list)