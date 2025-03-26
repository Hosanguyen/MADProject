from fastapi import APIRouter, HTTPException
from app.models.StatisticTypeModel import StatisticTypeModel
from app.models.StatisticDataModel import StatisticDataModel
from app.services.StatisticDataService import StatisticDataService
from app.services.StatisticTypeService import StatisticTypeService
from app.schemas.StatisticDataSchema import StatisticDataCreate
from typing import List

router = APIRouter(tags=["statistic"])

### API Statistic Type ###
@router.post("/statistic-types", response_model=StatisticTypeModel)
async def create_statistic_type(statType: StatisticTypeModel):
    return await StatisticTypeService.create(statType)

@router.get("/statistic-types", response_model=List[StatisticTypeModel])
async def get_statistic_types():
    return await StatisticTypeService.getAll()

@router.get("/statistic-types/{statId}", response_model=StatisticTypeModel)
async def get_statistic_type(statId: str):
    stat = await StatisticTypeService.getById(statId)
    if not stat:
        raise HTTPException(status_code=404, detail="Statistic Type not found")
    return stat

@router.put("/statistic-types/{statId}", response_model=StatisticTypeModel)
async def update_statistic_type(statId: str, stat_update: StatisticTypeModel):
    updated_stat = await StatisticTypeService.update(statId, stat_update)
    if not updated_stat:
        raise HTTPException(status_code=404, detail="Statistic Type not found")
    return updated_stat

@router.delete("/statistic-types/{statId}")
async def delete_statistic_type(statId: str):
    if not await StatisticTypeService.delete(statId):
        raise HTTPException(status_code=404, detail="Statistic Type not found")
    return {"message": "Deleted successfully"}

### API Statistic Data ###
@router.post("/statistic-data", response_model=StatisticDataModel)
async def create_statistic_data(stat_data: StatisticDataCreate):
    return await StatisticDataService.create(stat_data)

@router.get("/statistic-data", response_model=List[StatisticDataModel])
async def get_statistic_data():
    return await StatisticDataService.getAll()

@router.get("/statistic-data/getByType/{statisticType}", response_model=List[StatisticDataModel])
async def get_statistic_data(statisticType: str):
    return await StatisticDataService.getByType(statisticType)

@router.get("/statistic-data/{dataId}", response_model=StatisticDataModel)
async def get_statistic_data_by_id(dataId: str):
    data = await StatisticDataService.getById(dataId)
    if not data:
        raise HTTPException(status_code=404, detail="Statistic Data not found")
    return data

@router.put("/statistic-data/{dataId}", response_model=StatisticDataModel)
async def update_statistic_data(dataId: str, dataUpdate: StatisticDataModel):
    updated_data = await StatisticDataService.update(dataId, dataUpdate)
    if not updated_data:
        raise HTTPException(status_code=404, detail="Statistic Data not found")
    return updated_data

@router.delete("/statistic-data/{dataId}")
async def delete_statistic_data(dataId: str):
    if not await StatisticDataService.delete(dataId):
        raise HTTPException(status_code=404, detail="Statistic Data not found")
    return {"message": "Deleted successfully"}
