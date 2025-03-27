from fastapi import APIRouter, HTTPException
from app.services.ItemService import ItemService
from app.models.ItemModel import ItemModel
from app.schemas.ItemSchema import ItemCreate, ItemUpdateQuantity
from typing import Optional, List

router = APIRouter(tags=["item"])

@router.post("/item/add", response_model=ItemModel)
async def create_item(item: ItemCreate):
    return await ItemService.create(item)


@router.get("/item", response_model=List[ItemModel])
async def get_all():
    return await ItemService.getAll()

@router.get("/item/getByType/{itemType}", response_model=List[ItemModel])
async def get_by_type(itemType: int):
    return await ItemService.getByType(itemType)

@router.get("/item/getById/{itemId}", response_model=ItemModel)
async def get_by_id(itemId: int):
    return await ItemService.getById(itemId)

@router.put("/item/update/")
async def update(item: ItemModel):
    data = await ItemService.update(item)
    return {"message": "Updated successfully", "data": data}

@router.put("/item/changeQuantity")
async def change_quantity(item: ItemUpdateQuantity):
    if(await ItemService.changeQuantity(item.itemId, item.quantity)):
        return {"message": "Updated successfully"}
    else:
        {"message": "Updated Failed"}

@router.delete("/item/delete/{itemId}")
async def delete(itemId: int):
    if not await ItemService.delete(itemId):
        raise HTTPException(status_code=404, detail="Statistic Data not found")
    return {"message": "Deleted successfully"}
