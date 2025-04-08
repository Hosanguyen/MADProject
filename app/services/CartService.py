import aiomysql
from typing import Optional, List
from uuid import UUID
from app.core.database import Database
from app.services.CartItemService import CartItemService
from app.models.CartModel import CartModel
from app.models.CartItemModel import CartItemModel

class CartService:
    db = Database()
    dbCart = "cart"

    @staticmethod
    async def create(cart: CartModel) -> bool:
        conn = await CartService.db.acquire()
        query = f"INSERT INTO {CartService.dbCart} (userid) VALUES (%s)"
        values = (cart.userId,)
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
    async def get() -> List[CartModel]:
        conn = await CartService.db.acquire()
        query = f"SELECT id, userid FROM {CartService.dbCart}"
        try:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query)
                datas= await cursor.fetchall()
        finally:
            await conn.ensure_closed()
        if not datas:
            return None
        result = []
        for data in datas:
            cartItems = await CartItemService.getByCartId(data.get("id"))
            cart = CartModel(id=data.get("id"), userId=data.get("userid"), listItem=cartItems)
            result.append(cart)
        return result

    @staticmethod
    async def getByUserId(userId: UUID) -> List[CartModel]:
        conn = await CartService.db.acquire()
        query = f"SELECT id FROM {CartService.dbCart} WHERE userid = %s"
        values = (userId)
        try:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query, values)
                datas= await cursor.fetchall()
        finally:
            await conn.ensure_closed()
        if not datas:
            return None
        result = []
        for data in datas:
            cartItems = await CartItemService.getByCartId(data.get("id"))
            cart = CartModel(id=data.get("id"), userId=userId, listItem=cartItems)
            result.append(cart)
        return result


    @staticmethod
    async def getById(cartId: UUID) -> Optional[CartModel]:
        conn = await CartService.db.acquire()
        query = f"SELECT id, userid FROM {CartService.dbCart} WHERE id = %s"
        values = (cartId,)
        try:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query, values)
                data = await cursor.fetchone()
        finally:
            await conn.ensure_closed()
        if not data:
            return None
        cartItems = await CartItemService.getByCartId(cartId)
        return CartModel(id=cartId, userId=data["userid"], listItem=cartItems)

    @staticmethod
    async def delete(cartId: UUID) -> bool:
        conn = await CartService.db.acquire()
        query = f"DELETE FROM {CartService.dbCart} WHERE id = %s"
        values = (cartId,)
        try:
            async with conn.cursor() as cursor:
                await cursor.execute(query, values)
                await conn.commit()
                return cursor.rowcount > 0
        finally:
            await conn.ensure_closed()

    @staticmethod
    async def getTotal(cartId: UUID) -> float:
        cartItems: List[CartItemModel] = await CartItemService.getByCartId(cartId)
        total = 0.0
        from app.services.ItemService import ItemService
        for item in cartItems:
            total += item.item.price * item.quantity
        return total
