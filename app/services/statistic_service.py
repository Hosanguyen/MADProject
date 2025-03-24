from app.core.database import statistic_type_collection, statistic_data_collection
from app.models.statistic import StatisticTypeModel, StatisticDataModel, PyObjectId
from bson import ObjectId
from typing import List

### Service xử lý Statistic Type ###
async def create_statistic_type(stat_type: StatisticTypeModel):
    stat_dict = stat_type.dict(by_alias=True)  
    result = await statistic_type_collection.insert_one(stat_dict)
    stat_dict["_id"] = str(result.inserted_id)
    return stat_dict

async def get_statistic_types():
    stats = await statistic_type_collection.find().to_list(100)
    for stat in stats:
        stat["_id"] = str(stat["_id"])
    return stats

async def get_statistic_type(stat_id: str):
    stat = await statistic_type_collection.find_one({"_id": stat_id})
    print("check")
    print(stat_id)
    print(stat)
    if stat:
        stat["_id"] = str(stat["_id"])
    return stat

async def update_statistic_type(stat_id: str, stat_update: StatisticTypeModel):
    update_data = stat_update.dict(exclude_unset=True, by_alias=True)  
    result = await statistic_type_collection.update_one({"_id": stat_id}, {"$set": update_data})
    if result.modified_count == 0:
        return None
    return {**update_data, "_id": stat_id}

async def delete_statistic_type(stat_id: str):
    result = await statistic_type_collection.delete_one({"_id": stat_id})
    return result.deleted_count > 0

### Service xử lý Statistic Data ###
async def create_statistic_data(stat_data: StatisticDataModel):
    stat_dict = stat_data.dict(by_alias=True)  # Thay model_dump()
    result = await statistic_data_collection.insert_one(stat_dict)
    stat_dict["_id"] = str(result.inserted_id)
    return stat_dict

async def get_statistic_data():
    data = await statistic_data_collection.find().to_list(100)
    for d in data:
        d["_id"] = str(d["_id"])
    return data

async def get_statistic_data_by_id(data_id: str):
    data = await statistic_data_collection.find_one({"_id": data_id})
    if data:
        data["_id"] = str(data["_id"])
    return data

async def update_statistic_data(data_id: str, data_update: StatisticDataModel):
    update_data = data_update.dict(exclude_unset=True, by_alias=True)  # Thay model_dump()
    result = await statistic_data_collection.update_one({"_id": data_id}, {"$set": update_data})
    if result.modified_count == 0:
        return None
    return {**update_data, "_id": data_id}

async def delete_statistic_data(data_id: str):
    result = await statistic_data_collection.delete_one({"_id": data_id})
    return result.deleted_count > 0
