from fastapi import APIRouter, HTTPException
from app.models.StatisticTypeModel import StatisticTypeModel
from app.models.StatisticDataModel import StatisticDataModel
from app.services.StatisticDataService import StatisticDataService
from app.services.StatisticTypeService import StatisticTypeService
from app.schemas.StatisticDataSchema import StatisticDataCreate
from typing import List
from uuid import UUID

router = APIRouter(tags=["statistic"])

### API Statistic Type ###
@router.post("/statistic-types")
async def create_statistic_type(statType: StatisticTypeModel):
    if(await StatisticTypeService.create(statType)):
        return {"message": "Created successfully"}
    raise HTTPException(status_code=400, detail="Failed to create statistic data")

@router.get("/statistic-types", response_model=List[StatisticTypeModel])
async def get_statistic_types():
    return await StatisticTypeService.getAll()

@router.get("/statistic-types/{statId}", response_model=StatisticTypeModel)
async def get_statistic_type(statId: UUID):
    stat = await StatisticTypeService.getById(statId)
    if not stat:
        raise HTTPException(status_code=404, detail="Statistic Type not found")
    return stat

@router.put("/statistic-types/update", response_model=StatisticTypeModel)
async def update_statistic_type(stat_update: StatisticTypeModel):
    updated_stat = await StatisticTypeService.update(stat_update)
    if not updated_stat:
        raise HTTPException(status_code=404, detail="Statistic Type not found")
    return updated_stat

@router.delete("/statistic-types/{statId}")
async def delete_statistic_type(statId: UUID):
    if not await StatisticTypeService.delete(statId):
        raise HTTPException(status_code=404, detail="Statistic Type not found")
    return {"message": "Deleted successfully"}

### API Statistic Data ###
@router.post("/statistic-data")
async def create_statistic_data(stat_data: StatisticDataCreate):
    success = await StatisticDataService.create(stat_data)
    
    if success:
        return {"message": "Created successfully"}
    
    # Nếu thất bại, ném lỗi HTTP 400
    raise HTTPException(status_code=400, detail="Failed to create statistic data")

@router.get("/statistic-data", response_model=List[StatisticDataModel])
async def get_statistic_data():
    return await StatisticDataService.getAll()

@router.get("/statistic-data/getByType/{statisticType}", response_model=List[StatisticDataModel])
async def get_statistic_data(statisticType: UUID):
    return await StatisticDataService.getByType(statisticType)

@router.get("/statistic-data/{dataId}", response_model=StatisticDataModel)
async def get_statistic_data_by_id(dataId: UUID):
    data = await StatisticDataService.getById(dataId)
    if not data:
        raise HTTPException(status_code=404, detail="Statistic Data not found")
    return data

@router.put("/statistic-data/update", response_model=StatisticDataModel)
async def update_statistic_data(dataUpdate: StatisticDataModel):
    updated_data = await StatisticDataService.update(dataUpdate)
    if not updated_data:
        raise HTTPException(status_code=404, detail="Statistic Data not found")
    return updated_data

@router.delete("/statistic-data/{dataId}")
async def delete_statistic_data(dataId: UUID):
    if not await StatisticDataService.delete(dataId):
        raise HTTPException(status_code=404, detail="Statistic Data not found")
    return {"message": "Deleted successfully"}
