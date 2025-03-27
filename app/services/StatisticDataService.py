import aiomysql
from app.core.database import Database
from app.models.StatisticDataModel import StatisticDataModel
from app.schemas.StatisticDataSchema import StatisticDataCreate
from typing import List, Optional
from uuid import UUID

class StatisticDataService:
    db = Database()  
    dbStatisticData = "pet_statistic"
    @staticmethod
    async def create(statData: StatisticDataCreate) -> bool:
        conn = await StatisticDataService.db.acquire()
        query = f"INSERT INTO {StatisticDataService.dbStatisticData} (value, recorded_at, petid, statistic_typeid) VALUES (%s, %s, %s, %s)"
        values = (statData.value, statData.recorded_at, statData.petId, statData.statisticTypeId)
        try:
            async with conn.cursor() as cursor:
                await cursor.execute(query,values)
                await conn.commit()
        except:
            return False
        finally:
            conn.close()
        
        return True

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
    
    async def getByType(statisticTypeId: UUID) -> List[StatisticDataModel]:
        conn = await StatisticDataService.db.acquire()
        query = f"SELECT id, value, recorded_at FROM {StatisticDataService.dbStatisticData} WHERE statistic_typeid = %s"
        values = (statisticTypeId) 
        try:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query, values)
                data = await cursor.fetchall()
        finally:
            conn.close()

        return [StatisticDataModel(**d) for d in data]

    @staticmethod
    async def getById(dataId: UUID) -> Optional[StatisticDataModel]:
        conn = await StatisticDataService.db.acquire()
        query = f"SELECT id, value, recorded_at FROM {StatisticDataService.dbStatisticData} WHERE id = %s"
        values = (dataId)
        try:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query, values)
                data = await cursor.fetchone()
        finally:
            conn.close()

        return StatisticDataModel(**data) if data else None

    @staticmethod
    async def update(dataUpdate: StatisticDataModel) -> Optional[StatisticDataModel]:
        conn = await StatisticDataService.db.acquire()
        query = f"UPDATE {StatisticDataService.dbStatisticData} SET value = %s, recorded_at = %s WHERE id = %s"
        values = (dataUpdate.value, dataUpdate.recorded_at, str(dataUpdate.id))
        try:
            async with conn.cursor() as cursor:
                await cursor.execute(query,values)
                await conn.commit()
                if cursor.rowcount == 0:
                    return None
        finally:
            conn.close()

        return dataUpdate

    @staticmethod
    async def delete(dataId: UUID) -> bool:
        conn = await StatisticDataService.db.acquire()
        query = f"DELETE FROM {StatisticDataService.dbStatisticData} WHERE id = %s"
        values =  (dataId)
        try:
            async with conn.cursor() as cursor:
                await cursor.execute(query, values)
                await conn.commit()
                return cursor.rowcount > 0
        finally:
            conn.close()
