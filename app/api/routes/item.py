from fastapi import APIRouter, HTTPException
from app.services.ItemService import ItemService
from app.models.ItemModel import ItemModel
from app.schemas.ItemSchema import ItemCreate, ItemUpdateQuantity
from typing import Optional, List
from uuid import UUID

router = APIRouter(tags=["item"])

@router.post("/item/add")
async def create_item(item: ItemCreate):
    success = await ItemService.create(item)
    
    if success:
        return {"message": "Created successfully"}
    
    raise HTTPException(status_code=400, detail="Failed to create item data")


@router.get("/item", response_model=List[ItemModel])
async def get_all():
    return await ItemService.getAll()

@router.get("/item/getByType/{itemType}", response_model=List[ItemModel])
async def get_by_type(itemType: UUID):
    return await ItemService.getByType(itemType)

@router.get("/item/getById/{itemId}", response_model=ItemModel)
async def get_by_id(itemId: UUID):
    return await ItemService.getById(itemId)

@router.put("/item/update/")
async def update(item: ItemModel):
    data = await ItemService.update(item)
    return {"message": "Updated successfully", "data": data}

@router.put("/item/changeQuantity")
async def change_quantity(item: ItemUpdateQuantity):
    success = await ItemService.changeQuantity(item.itemId, item.quantity)
    
    if success:
        return {"message": "Updated successfully"}
    
    raise HTTPException(status_code=400, detail="Failed to update item data")

@router.delete("/item/delete/{itemId}")
async def delete(itemId: UUID):
    if not await ItemService.delete(itemId):
        raise HTTPException(status_code=404, detail="Statistic Data not found")
    return {"message": "Deleted successfully"}
