import aiomysql
from app.core.database import Database
from app.models.StatisticDataModel import StatisticDataModel
from typing import List, Optional

class StatisticDataService:
    db = Database()  

    @staticmethod
    async def create(statData: StatisticDataModel) -> StatisticDataModel:
        conn = await StatisticDataService.db.acquire()
        try:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    "INSERT INTO tblStatisticData (statisticTypeId, value, timestamp) VALUES (%s, %s, %s)",
                    (statData.statisticTypeId, statData.value, statData.timestamp),
                )
                await conn.commit()
                statData.id = cursor.lastrowid
        finally:
            conn.close()
        return statData

    @staticmethod
    async def getAll() -> List[StatisticDataModel]:
        conn = await StatisticDataService.db.acquire()
        try:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute("SELECT id, statisticTypeId, value, timestamp FROM tblStatisticData")
                data = await cursor.fetchall()
        finally:
            conn.close()

        return [StatisticDataModel(**d) for d in data]

    @staticmethod
    async def getById(dataId: int) -> Optional[StatisticDataModel]:
        conn = await StatisticDataService.db.acquire()
        try:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute("SELECT id, statisticTypeId, value, timestamp FROM tblStatisticData WHERE id = %s", (dataId,))
                data = await cursor.fetchone()
        finally:
            conn.close()

        return StatisticDataModel(**data) if data else None

    @staticmethod
    async def update(dataId: int, dataUpdate: StatisticDataModel) -> Optional[StatisticDataModel]:
        conn = await StatisticDataService.db.acquire()
        try:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    "UPDATE tblStatisticData SET statisticTypeId = %s, value = %s, timestamp = %s WHERE id = %s",
                    (dataUpdate.statisticTypeId, dataUpdate.value, dataUpdate.timestamp, dataId),
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
        try:
            async with conn.cursor() as cursor:
                await cursor.execute("DELETE FROM tblStatisticData WHERE id = %s", (dataId,))
                await conn.commit()
                return cursor.rowcount > 0
        finally:
            conn.close()
