import aiomysql
from app.core.database import Database
from app.models.StatisticDataModel import StatisticDataModel
from app.schemas.StatisticDataSchema import StatisticDataCreate
from typing import List, Optional

class StatisticDataService:
    db = Database()  
    dbStatisticData = "pet_statistic"
    @staticmethod
    async def create(statData: StatisticDataCreate) -> StatisticDataModel:
        conn = await StatisticDataService.db.acquire()
        query = f"INSERT INTO {StatisticDataService.dbStatisticData} (value, recorded_at, petid, statistic_typeid) VALUES (%s, %s, %s, %s)"
        try:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    query,
                    (statData.value, statData.recorded_at, statData.petId, statData.statisticTypeId),
                )
                await conn.commit()
                statData.id = cursor.lastrowid
        finally:
            conn.close()
        
        return StatisticDataModel(id=statData.id, value=statData.value, recorded_at=statData.recorded_at)

    @staticmethod
    async def getAll() -> List[StatisticDataModel]:
        conn = await StatisticDataService.db.acquire()
        query = f"SELECT id, value, recorded_at FROM {StatisticDataService.dbStatisticData}"
        try:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query)
                data = await cursor.fetchall()
        finally:
            conn.close()

        return [StatisticDataModel(**d) for d in data]
    
    async def getByType(statisticTypeId: int) -> List[StatisticDataModel]:
        conn = await StatisticDataService.db.acquire()
        query = f"SELECT id, value, recorded_at FROM {StatisticDataService.dbStatisticData} WHERE statistic_typeid = %s"
        try:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query, (statisticTypeId,))
                data = await cursor.fetchall()
        finally:
            conn.close()

        return [StatisticDataModel(**d) for d in data]

    @staticmethod
    async def getById(dataId: int) -> Optional[StatisticDataModel]:
        conn = await StatisticDataService.db.acquire()
        query = f"SELECT id, value, recorded_at FROM {StatisticDataService.dbStatisticData} WHERE id = %s"
        try:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query, (dataId,))
                data = await cursor.fetchone()
        finally:
            conn.close()

        return StatisticDataModel(**data) if data else None

    @staticmethod
    async def update(dataId: int, dataUpdate: StatisticDataModel) -> Optional[StatisticDataModel]:
        conn = await StatisticDataService.db.acquire()
        query = f"UPDATE {StatisticDataService.dbStatisticData} SET value = %s, recorded_at = %s WHERE id = %s"
        try:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    query,
                    (dataUpdate.value, dataUpdate.recorded_at, dataId),
                )
                await conn.commit()
                if cursor.rowcount == 0:
                    return None
        finally:
            conn.close()

        dataUpdate.id = dataId
        return dataUpdate

    @staticmethod
    async def delete(dataId: int) -> bool:
        conn = await StatisticDataService.db.acquire()
        query = f"DELETE FROM {StatisticDataService.dbStatisticData} WHERE id = %s"
        try:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (dataId,))
                await conn.commit()
                return cursor.rowcount > 0
        finally:
            conn.close()
