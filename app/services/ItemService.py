import os
import uuid
import aiofiles
import aiomysql
from typing import Optional, List

from fastapi import UploadFile
from app.core.database import Database
from app.models.ItemModel import ItemModel
from app.schemas.ItemSchema import ItemCreate, ItemUpdate
from uuid import UUID
from app.core.config import settings
from app.core.database import db

IMAGE_ITEM = f"{settings.IMAGE_DIR}items/"


class ItemService:
    db = db
    dbItem = "item"

    @staticmethod
    async def saveImage(image: UploadFile) -> Optional[str]:
        if not image:
            return None
        filename = f"{uuid.uuid4()}.{image.filename.split('.')[-1]}"
        save_path = f"{IMAGE_ITEM}{filename}"

        try:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            async with aiofiles.open(save_path, "wb") as out_file:
                content = await image.read()
                await out_file.write(content)
            return save_path, filename.split('.')[0]
        except Exception as e:
            print(f"Image save error: {e}")
            return None

    @staticmethod
    async def create(item: ItemCreate) -> bool:
        conn = await ItemService.db.acquire()
        query = f"INSERT INTO {ItemService.dbItem} (id, name, price, quantity, description, manufacturer, item_typeid, image_url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        filename, id = await ItemService.saveImage(item.image)
        values = (id, item.name, item.price, item.quantity, item.description, item.manufacturer, item.itemTypeId, filename)
        print(values)
        try:
            async with conn.cursor() as cursor:
                await cursor.execute(query, values)
                await conn.commit()

        except:
            return False
        finally:
            await conn.ensure_closed()
        return True

    @staticmethod
    async def getAll() -> List[ItemModel]:
        conn = await db.acquire()
        query = f"SELECT id, name, price, quantity, description, manufacturer, image_url FROM {ItemService.dbItem}"
        try:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query)
                datas = await cursor.fetchall()
        finally:
            await conn.ensure_closed()
        return [ItemModel(**data) for data in datas]
    
    @staticmethod
    async def getByType(itemType: UUID) -> List[ItemModel]:
        conn = await ItemService.db.acquire()
        query = f"SELECT id, name, price, quantity, description, manufacturer, image_url FROM {ItemService.dbItem} WHERE item_typeid = %s"
        values = (itemType)
        try:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query, values)
                datas = await cursor.fetchall()
        finally:
            await conn.ensure_closed()
        return [ItemModel(**data) for data in datas]
    
    @staticmethod
    async def getById(itemId: UUID) -> ItemModel:
        conn = await ItemService.db.acquire()
        query = f"SELECT id, name, price, quantity, description, manufacturer, image_url FROM {ItemService.dbItem} WHERE id = %s"
        values = (itemId)
        try:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query, values)
                data = await cursor.fetchone()
        finally:
            await conn.ensure_closed()
        return ItemModel(**data)
    
    @staticmethod
    async def update(item: ItemUpdate) -> bool:
        conn = await ItemService.db.acquire()
        query = f"UPDATE {ItemService.dbItem} SET name = %s, price = %s, quantity = %s, description = %s, manufacturer = %s, item_typeid = %s, image_url = %s WHERE id = %s"
        if(item.image):
            filename, tmp = await ItemService.saveImage(item.image)
            values = (item.name, item.price, item.quantity, item.description, item.manufacturer, item.itemTypeId, filename, str(item.id))
        else:
            query = f"UPDATE {ItemService.dbItem} SET name = %s, price = %s, quantity = %s, description = %s, manufacturer = %s, item_typeid = %s WHERE id = %s"
            values = (item.name, item.price, item.quantity, item.description, item.manufacturer, item.itemTypeId, str(item.id))

        print(values)
        try:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query, values)
                await conn.commit()
        except Exception as e:
            print(f"Lỗi khi update DB: {e}")
            return False

        finally:
            await conn.ensure_closed()
        return True
    
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
            await conn.ensure_closed()
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
            await conn.ensure_closed()
