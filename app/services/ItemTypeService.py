from app.models.ItemTypeModel import ItemTypeModel
from typing import Optional, List
from app.core.database import Database
import aiomysql
from app.services.ItemService import ItemService
from uuid import UUID

class ItemTypeService:
    db = Database()
    dbItemtype = "item_type"

    @staticmethod
    async def create(itemType: ItemTypeModel) -> bool:
        conn = await ItemTypeService.db.acquire()
        query = f"INSERT INTO {ItemTypeService.dbItemtype} (name, unit, note) VALUES (%s, %s, %s)"
        values = (itemType.name, itemType.unit, itemType.note)

        try:
            async with conn.cursor() as cursor:
                await cursor.execute(query, values)
                await conn.commit()
        except:
            return False
        finally:
            conn.close()
        return True
    
    @staticmethod
    async def getAll() -> List[ItemTypeModel]:
        conn = await ItemTypeService.db.acquire()
        query = f"SELECT id, name, unit, note FROM {ItemTypeService.dbItemtype}"

        try:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query)
                data = await cursor.fetchall()
        finally:
            conn.close()
        result = []
        for d in data:
            itemType = ItemTypeModel(**d)
            itemType.listItem = await ItemService.getByType(itemType.id)
            result.append(d)
        return result
    
    @staticmethod
    async def getById(itemTypeId: UUID) -> ItemTypeModel:
        conn = await ItemTypeService.db.acquire()
        query = f"SELECT id, name, unit, note FROM {ItemTypeService.dbItemtype} WHERE id = %s"
        values = (itemTypeId)

        try:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query, values)
                data = await cursor.fetchone()
        finally:
            conn.close()
        itemType = ItemTypeModel(**data)
        itemType.listItem = await ItemService.getByType(itemType.id)
        return itemType
    
    @staticmethod
    async def update(itemType: ItemTypeModel) -> bool:
        conn = await ItemTypeService.db.acquire()
        query = f"UPDATE {ItemTypeService.dbItemtype} SET name = %s, unit =  %s, note = %s WHERE id = %s"
        values = (itemType.name, itemType.unit, itemType.note, str(itemType.id))

        try: 
            async with conn.cursor() as cursor:
                await cursor.execute(query, values)
                await conn.commit()
        except:
            return False
        finally:
            conn.close()
        
        return True
    
    @staticmethod
    async def delete(itemTypeId: UUID) -> bool:
        print(itemTypeId)
        conn = await ItemTypeService.db.acquire()
        query = f"DELETE FROM {ItemTypeService.dbItemtype} WHERE id = %s"
        values = (itemTypeId)

        try:
            async with conn.cursor() as cursor:
                await cursor.execute(query, values)
                await conn.commit()
        except:
            return False
        finally:
            conn.close()

        return True