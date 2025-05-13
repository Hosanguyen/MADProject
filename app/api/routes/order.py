from fastapi import APIRouter
from uuid import UUID
from typing import List

from app.services.OrderService import OrderService
from app.schemas.OrderSchema import OrderCreate
from app.models.OrderModel import OrderModel
from app.models.OrderItemModel import OrderItemModel
from app.schemas.OrderSchema import OrderInit
router = APIRouter(prefix='/order', tags=["Order"])

@router.post("/")
async def create_cart_item(order: OrderCreate):
    await OrderService.create(order)
    return {"message": "Successfully created order item"}

@router.get("/", response_model=List[OrderModel])
async def get_all_cart_items():
    return await OrderService.getAll()

@router.get("/user/{userId}", response_model=List[OrderModel])
async def get_cart_items_by_cart_id(userId: UUID):
    return await OrderService.getByUserId(userId)

@router.get("/{orderId}", response_model=OrderModel)
async def get_cart_item_by_id(orderId: UUID):
    return await OrderService.getById(orderId)

@router.delete("/{orderId}")
async def delete_cart_item(orderId: UUID):
    await OrderService.delete(orderId)
    return {"message": "Deleted successfully"}

@router.post("/create")
async def create_order(order: OrderInit):
    await OrderService.createOrder(order)
    return {"message": "Successfully created order item"}