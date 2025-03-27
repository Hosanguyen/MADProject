from pydantic import BaseModel, Field
from typing import Optional, List
from app.models.CartItemModel import CartItemModel

class CartModel(BaseModel):
    id: Optional[int] = None
    listItem: List[CartItemModel] = Field(default_factory=list)