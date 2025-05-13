import aiomysql
from app.core.database import Database
from app.models.StatisticTypeModel import StatisticTypeModel
from typing import List, Optional
from app.services.StatisticDataService import StatisticDataService
from uuid import UUID

class StatisticTypeService:
    db = Database()  
    dbStatisticType = "statistic_type"
    @staticmethod
    async def create(statType: StatisticTypeModel) -> bool:
        conn = await StatisticTypeService.db.acquire()
        query = f"INSERT INTO {StatisticTypeService.dbStatisticType} (name, unit, description) VALUES (%s, %s, %s)"
        values = (statType.name, statType.unit, statType.description)
        try:
            async with conn.cursor() as cursor:
                await cursor.execute(query,values)
                await conn.commit()
        except:
                return False
        finally:
            await StatisticTypeService.db.release(conn)
        return True

    @staticmethod
    async def getAll() -> List[StatisticTypeModel]:
        conn = await StatisticTypeService.db.acquire()
        query = f"SELECT id, name, description, unit FROM {StatisticTypeService.dbStatisticType}"
        try:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query)
                stats = await cursor.fetchall()
        finally:
            await StatisticTypeService.db.release(conn)
        result = []
        for stat in stats:
            data = StatisticTypeModel(**stat)
            data.listStatisticData = await StatisticDataService.getByType(data.id)
            result.append(data)
        return result

    @staticmethod
    async def getById(statId: UUID) -> Optional[StatisticTypeModel]:
        conn = await StatisticTypeService.db.acquire()
        query = f"SELECT id, name, description, unit FROM {StatisticTypeService.dbStatisticType} WHERE id = %s"
        values = (statId)
        try:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query, values)
                stat = await cursor.fetchone()
        finally:
            await StatisticTypeService.db.release(conn)

        data = StatisticTypeModel(**stat)
        data.listStatisticData = await StatisticDataService.getByType(data.id)
        return data

    @staticmethod
    async def update(statUpdate: StatisticTypeModel) -> Optional[StatisticTypeModel]:
        conn = await StatisticTypeService.db.acquire()
        query = f"UPDATE {StatisticTypeService.dbStatisticType} SET name = %s, description = %s, unit = %s WHERE id = %s"
        values = (statUpdate.name, statUpdate.description, statUpdate.unit, str(statUpdate.id))
        try:
            async with conn.cursor() as cursor:
                await cursor.execute(query,values)
                await conn.commit()
                if cursor.rowcount == 0:
                    return None
        finally:
            await StatisticTypeService.db.release(conn)

        return statUpdate

    @staticmethod
    async def delete(statId: UUID) -> bool:
        conn = await StatisticTypeService.db.acquire()
        query = f"DELETE FROM {StatisticTypeService.dbStatisticType} WHERE id = %s"
        values = (statId)
        try:
            async with conn.cursor() as cursor:
                await cursor.execute(query, values)
                await conn.commit()
                return cursor.rowcount > 0
        finally:
            await StatisticTypeService.db.release(conn)
