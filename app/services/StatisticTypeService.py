import aiomysql
from app.core.database import Database
from app.models.StatisticTypeModel import StatisticTypeModel
from typing import List, Optional

class StatisticTypeService:
    db = Database()  

    @staticmethod
    async def create(statType: StatisticTypeModel) -> StatisticTypeModel:
        conn = await StatisticTypeService.db.acquire()
        try:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    "INSERT INTO tblStatisticType (name, description, unit) VALUES (%s, %s, %s)",
                    (statType.name, statType.description, statType.unit),
                )
                await conn.commit()
                statType.id = cursor.lastrowid
        finally:
            conn.close()
        return statType

    @staticmethod
    async def getAll() -> List[StatisticTypeModel]:
        conn = await StatisticTypeService.db.acquire()
        try:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute("SELECT id, name, description, unit FROM tblStatisticType")
                stats = await cursor.fetchall()
        finally:
            conn.close()

        return [StatisticTypeModel(**stat) for stat in stats]

    @staticmethod
    async def getById(statId: int) -> Optional[StatisticTypeModel]:
        conn = await StatisticTypeService.db.acquire()
        try:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute("SELECT id, name, description, unit FROM tblStatisticType WHERE id = %s", (statId,))
                stat = await cursor.fetchone()
        finally:
            conn.close()

        return StatisticTypeModel(**stat) if stat else None

    @staticmethod
    async def update(statId: int, statUpdate: StatisticTypeModel) -> Optional[StatisticTypeModel]:
        conn = await StatisticTypeService.db.acquire()
        try:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    "UPDATE tblStatisticType SET name = %s, description = %s, unit = %s WHERE id = %s",
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
        try:
            async with conn.cursor() as cursor:
                await cursor.execute("DELETE FROM tblStatisticType WHERE id = %s", (statId,))
                await conn.commit()
                return cursor.rowcount > 0
        finally:
            conn.close()
