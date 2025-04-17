from typing import Optional, List
from fastapi import APIRouter, HTTPException
from app.models.ItemTypeModel import ItemTypeModel
from app.services.ItemTypeService import ItemTypeService
from uuid import UUID

router = APIRouter(tags=["item_type"])

@router.post("/item_type/add")
async def create(itemType: ItemTypeModel):
    success = await ItemTypeService.create(itemType)
    
    if success:
        return {"message": "Created successfully"}
    
    # Nếu thất bại, ném lỗi HTTP 400
    raise HTTPException(status_code=400, detail="Failed to create item type data")

@router.get("/item_type/get", response_model=List[ItemTypeModel])
async def get_all():
    return await ItemTypeService.getAll()

@router.get("/item_type/getById/{itemTypeId}", response_model=ItemTypeModel)
async def get_by_id(itemTypeId: UUID):
    return await ItemTypeService.getById(itemTypeId)

@router.put("/item_type/update")
async def update(itemType: ItemTypeModel):
    success = await ItemTypeService.update(itemType)
    
    if success:
        return {"message": "Updated successfully"}
    
    # Nếu thất bại, ném lỗi HTTP 400
    raise HTTPException(status_code=400, detail="Failed to update item type data")

@router.delete("/item_type/delete/{itemTypeId}")
async def delete(itemTypeId: UUID):
    if not await ItemTypeService.delete(itemTypeId):
        raise HTTPException(status_code=404, detail="Statistic Data not found")
    return {"message": "Deleted successfully"}
