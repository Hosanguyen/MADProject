from fastapi import APIRouter
from uuid import UUID
from typing import List

from app.services.CartItemService import CartItemService
from app.schemas.CartItemSchema import CartItemCreate, CartItemUpdateQuantity
from app.models.CartItemModel import CartItemModel

router = APIRouter(prefix='/cart-item', tags=["Cart Items"])

@router.post("/")
async def create_cart_item(cart_item: CartItemCreate):
    await CartItemService.create(cart_item)
    return {"message": "Successfully created cart item"}

@router.get("/", response_model=List[CartItemModel])
async def get_all_cart_items():
    return await CartItemService.getAll()

@router.get("/cart/{cart_id}", response_model=List[CartItemModel])
async def get_cart_items_by_cart_id(cart_id: UUID):
    return await CartItemService.getByCartId(cart_id)

@router.get("/{cart_item_id}", response_model=CartItemModel)
async def get_cart_item_by_id(cart_item_id: UUID):
    return await CartItemService.getById(cart_item_id)

@router.patch("/{cart_item_id}/quantity")
async def update_quantity(cart_item_id: UUID, quantity_update: CartItemUpdateQuantity):
    await CartItemService.changeQuantity(cart_item_id, quantity_update.quantity)
    return {"message": "Quantity updated successfully"}

@router.delete("/{cart_item_id}")
async def delete_cart_item(cart_item_id: UUID):
    await CartItemService.delete(cart_item_id)
    return {"message": "Deleted successfully"}

@router.delete("/remove/{cart_item_id}")
async def remove_cart_item(cart_item_id:UUID):
    await CartItemService.remove(cart_item_id)
    return {"message:" "Removed successfully"}