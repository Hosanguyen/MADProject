from fastapi import APIRouter
from uuid import UUID
from typing import List

from app.services.OrderItemService import OrderItemService
from app.schemas.OrderItemSchema import OrderItemCreate
from app.models.OrderItemModel import OrderItemModel

router = APIRouter(prefix='/order-item', tags=["Order Items"])

@router.post("/")
async def create_cart_item(cart_item: OrderItemCreate):
    await OrderItemService.create(cart_item)
    return {"message": "Successfully created order item"}

@router.get("/", response_model=List[OrderItemModel])
async def get_all_cart_items():
    return await OrderItemService.getAll()

@router.get("/order/{orderId}", response_model=List[OrderItemModel])
async def get_cart_items_by_orderId(orderId: UUID):
    return await OrderItemService.getByOrderId(orderId)

@router.get("/{orderItemId}", response_model=OrderItemModel)
async def get_cart_item_by_id(orderItemId: UUID):
    return await OrderItemService.getById(orderItemId)

@router.delete("/{orderItemId}")
async def delete_cart_item(orderItemId: UUID):
    await OrderItemService.delete(orderItemId)
    return {"message": "Deleted successfully"}
