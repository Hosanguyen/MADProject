from fastapi import APIRouter, HTTPException
from uuid import UUID
from app.models.CartModel import CartModel
from app.services.CartService import CartService
from app.schemas.CartItemSchema import CartItemCreate
router = APIRouter(prefix='/cart', tags=["Cart"])

@router.post("/")
async def create_cart(cart: CartModel):
    success = await CartService.create(cart)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to create cart")
    return {"message": "Successfully"}

@router.get("/", response_model=list[CartModel])
async def get_all():
    cart = await CartService.get()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart

@router.get("/user/{userId}", response_model=list[CartModel])
async def get_by_userid(userId: UUID):
    cart = await CartService.getByUserId(userId)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart


@router.get("/{cart_id}", response_model=CartModel)
async def get_cart(cart_id: UUID):
    cart = await CartService.getById(cart_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart

@router.post("/add_to_cart")
async def add_to_cart(cartItem: CartItemCreate):
    success = await CartService.add_to_cart(cartItem=cartItem)
    if(not success):
        raise HTTPException(status_code=500, detail="Failed to add to cart")
    return {"message": "Successfully"}

@router.delete("/{cart_id}")
async def delete_cart(cart_id: UUID):
    deleted = await CartService.delete(cart_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Cart not found or already deleted")
    return {"message": "Successfully"}

@router.get("/{cart_id}/total", response_model=float)
async def get_cart_total(cart_id: UUID):
    try:
        total = await CartService.getTotal(cart_id)
        return total
    except:
        raise HTTPException(status_code=500, detail="Failed to calculate cart total")
