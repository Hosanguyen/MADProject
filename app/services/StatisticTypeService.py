import aiomysql
from app.core.database import Database
from app.models.StatisticTypeModel import StatisticTypeModel
from typing import List, Optional
from app.services.StatisticDataService import StatisticDataService
class StatisticTypeService:
    db = Database()  
    dbStatisticType = "statistic_type"
    @staticmethod
    async def create(statType: StatisticTypeModel) -> StatisticTypeModel:
        conn = await StatisticTypeService.db.acquire()
        query = f"INSERT INTO {StatisticTypeService.dbStatisticType} (name, unit, description) VALUES (%s, %s, %s)"
        try:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    query,
                    (statType.name, statType.unit, statType.description),
                )
                await conn.commit()
                statType.id = cursor.lastrowid
        finally:
            conn.close()
        return statType

    @staticmethod
    async def getAll() -> List[StatisticTypeModel]:
        conn = await StatisticTypeService.db.acquire()
        query = f"SELECT id, name, description, unit FROM {StatisticTypeService.dbStatisticType}"
        try:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query)
                stats = await cursor.fetchall()
        finally:
            conn.close()
        result = []
        for stat in stats:
            data = StatisticTypeModel(**stat)
            data.listStatisticData = await StatisticDataService.getByType(data.id)
            result.append(data)
        return result

    @staticmethod
    async def getById(statId: int) -> Optional[StatisticTypeModel]:
        conn = await StatisticTypeService.db.acquire()
        query = f"SELECT id, name, description, unit FROM {StatisticTypeService.dbStatisticType} WHERE id = %s"
        try:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query, (statId))
                stat = await cursor.fetchone()
        finally:
            conn.close()

        data = StatisticTypeModel(**stat)
        data.listStatisticData = await StatisticDataService.getByType(data.id)
        return data

    @staticmethod
    async def update(statId: int, statUpdate: StatisticTypeModel) -> Optional[StatisticTypeModel]:
        conn = await StatisticTypeService.db.acquire()
        query = f"UPDATE {StatisticTypeService.dbStatisticType} SET name = %s, description = %s, unit = %s WHERE id = %s"
        try:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    query,
                    (statUpdate.name, statUpdate.description, statUpdate.unit, statId),
                )
                await conn.commit()
                if cursor.rowcount == 0:
                    return None
        finally:
            conn.close()

        statUpdate.id = statId
        return statUpdate

    @staticmethod
    async def delete(statId: int) -> bool:
        conn = await StatisticTypeService.db.acquire()
        query = f"DELETE FROM {StatisticTypeService.dbStatisticType} WHERE id = %s"
        try:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (statId))
                await conn.commit()
                return cursor.rowcount > 0
        finally:
            conn.close()
