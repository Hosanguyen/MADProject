from typing import Optional, List
from fastapi import APIRouter, HTTPException
from app.models.ItemTypeModel import ItemTypeModel
from app.services.ItemTypeService import ItemTypeService

router = APIRouter(tags=["item_type"])

@router.post("/item_type/add")
async def create(itemType: ItemTypeModel):
    if(await ItemTypeService.create(itemType)):
        return {"message": "Successfully"}
    else:
        return {"message": "Failed"}

@router.get("/item_type/get", response_model=List[ItemTypeModel])
async def get_all():
    return await ItemTypeService.getAll()

@router.get("/item_type/getById/{itemTypeId}", response_model=ItemTypeModel)
async def get_by_id(itemTypeId: int):
    return await ItemTypeService.getById(itemTypeId)

@router.put("/item_type/update")
async def update(itemType: ItemTypeModel):
    if(await ItemTypeService.update(itemType)):
        return {"message": "Updated successfully"}
    else:
        return {"message": "Updated Failed"}