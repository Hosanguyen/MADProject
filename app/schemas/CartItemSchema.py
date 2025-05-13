from app.models.CartItemModel import CartItemModel
from pydantic import BaseModel
from uuid import UUID

class CartItemCreate(CartItemModel):
    # cartId: UUID
    itemId: UUID
    userId: UUID

class CartItemUpdateQuantity(BaseModel):
    cartItemId: UUID
    quantity: int

class CartItemOrder(BaseModel):
    id: UUID
    quantity: int