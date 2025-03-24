from fastapi import APIRouter, HTTPException
from app.models.statistic import StatisticTypeModel, StatisticDataModel
import app.services.statistic_service as service
from typing import List

router = APIRouter(tags=["statistic"])

### API Statistic Type ###
@router.post("/statistic-types", response_model=StatisticTypeModel)
async def create_statistic_type(stat_type: StatisticTypeModel):
    return await service.create_statistic_type(stat_type)

@router.get("/statistic-types", response_model=List[StatisticTypeModel])
async def get_statistic_types():
    return await service.get_statistic_types()

@router.get("/statistic-types/{stat_id}", response_model=StatisticTypeModel)
async def get_statistic_type(stat_id: str):
    stat = await service.get_statistic_type(stat_id)
    if not stat:
        raise HTTPException(status_code=404, detail="Statistic Type not found")
    return stat

@router.put("/statistic-types/{stat_id}", response_model=StatisticTypeModel)
async def update_statistic_type(stat_id: str, stat_update: StatisticTypeModel):
    updated_stat = await service.update_statistic_type(stat_id, stat_update)
    if not updated_stat:
        raise HTTPException(status_code=404, detail="Statistic Type not found")
    return updated_stat

@router.delete("/statistic-types/{stat_id}")
async def delete_statistic_type(stat_id: str):
    if not await service.delete_statistic_type(stat_id):
        raise HTTPException(status_code=404, detail="Statistic Type not found")
    return {"message": "Deleted successfully"}

### API Statistic Data ###
@router.post("/statistic-data", response_model=StatisticDataModel)
async def create_statistic_data(stat_data: StatisticDataModel):
    return await service.create_statistic_data(stat_data)

@router.get("/statistic-data", response_model=List[StatisticDataModel])
async def get_statistic_data():
    return await service.get_statistic_data()

@router.get("/statistic-data/{data_id}", response_model=StatisticDataModel)
async def get_statistic_data_by_id(data_id: str):
    data = await service.get_statistic_data_by_id(data_id)
    if not data:
        raise HTTPException(status_code=404, detail="Statistic Data not found")
    return data

@router.put("/statistic-data/{data_id}", response_model=StatisticDataModel)
async def update_statistic_data(data_id: str, data_update: StatisticDataModel):
    updated_data = await service.update_statistic_data(data_id, data_update)
    if not updated_data:
        raise HTTPException(status_code=404, detail="Statistic Data not found")
    return updated_data

@router.delete("/statistic-data/{data_id}")
async def delete_statistic_data(data_id: str):
    if not await service.delete_statistic_data(data_id):
        raise HTTPException(status_code=404, detail="Statistic Data not found")
    return {"message": "Deleted successfully"}
