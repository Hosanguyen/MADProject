import aiomysql
from typing import Optional, List
from app.core.database import Database
from app.models.ItemModel import ItemModel
from app.schemas.ItemSchema import ItemCreate
from uuid import UUID

class ItemService:
    db = Database()
    dbItem = "item"

    @staticmethod
    async def create(item: ItemCreate) -> bool:
        conn = await ItemService.db.acquire()
        query = f"INSERT INTO {ItemService.dbItem} (name, price, quantity, description, manufacturer, item_typeid) VALUES (%s, %s, %s, %s, %s, %s)"

        try:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (item.name, item.price, item.quantity, item.description, item.manufacturer, item.itemTypeId))
                await conn.commit()
                return True
        finally:
            conn.close()
        return False

    @staticmethod
    async def getAll() -> List[ItemModel]:
        conn = await ItemService.db.acquire()
        query = f"SELECT id, name, price, quantity, description, manufacturer FROM {ItemService.dbItem}"
        try:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query)
                datas = await cursor.fetchall()
        finally:
            conn.close()
        return [ItemModel(**data) for data in datas]
    
    @staticmethod
    async def getByType(itemType: UUID) -> List[ItemModel]:
        conn = await ItemService.db.acquire()
        query = f"SELECT id, name, price, quantity, description, manufacturer FROM {ItemService.dbItem} WHERE item_typeid = %s"
        values = (itemType)
        try:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query, values)
                datas = await cursor.fetchall()
        finally:
            conn.close()
        return [ItemModel(**data) for data in datas]
    
    @staticmethod
    async def getById(itemId: UUID) -> ItemModel:
        conn = await ItemService.db.acquire()
        query = f"SELECT id, name, price, quantity, description, manufacturer FROM {ItemService.dbItem} WHERE id = %s"
        values = (itemId)
        try:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query, values)
                data = await cursor.fetchone()
        finally:
            conn.close()
        return data
    
    @staticmethod
    async def update(item: ItemModel) -> ItemModel:
        conn = await ItemService.db.acquire()
        query = f"UPDATE {ItemService.dbItem} SET name = %s, price = %s, quantity = %s, description = %s, manufacturer = %s WHERE id = %s"
        values = (item.name, item.price, item.quantity, item.description, item.manufacturer, item.id)
        
        try:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query, values)
                conn.commit()
        finally:
            conn.close()
        return item
    
    @staticmethod
    async def changeQuantity(itemId: UUID, quantity: int):
        conn = await ItemService.db.acquire()
        query = f"UPDATE {ItemService.dbItem} SET quantity = GREATEST(quantity + %s, 0 ) WHERE id = %s"
        values = (quantity, itemId)
        
        try:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query, values)
                await conn.commit()
        finally:
            conn.close()
        return True
    

    @staticmethod
    async def delete(itemId: UUID) -> bool:
        conn = await ItemService.db.acquire()
        query = f"DELETE FROM {ItemService.dbItem} WHERE id = %s"
        values = (itemId)
        try:
            async with conn.cursor() as cursor:
                await cursor.execute(query, values)
                await conn.commit()
                return cursor.rowcount > 0
        finally:
            conn.close()