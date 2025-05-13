import aiomysql
from typing import Optional, List
from uuid import UUID

from fastapi import HTTPException
from app.core.database import Database
from app.services.CartItemService import CartItemService
from app.models.CartModel import CartModel
from app.models.CartItemModel import CartItemModel
from app.schemas.CartItemSchema import CartItemCreate
from app.services.ItemService import ItemService
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
            await CartService.db.release(conn)
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
            await CartService.db.release(conn)
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
            await CartService.db.release(conn)
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
            await CartService.db.release(conn)
        if not data:
            return None
        cartItems = await CartItemService.getByCartId(cartId)
        return CartModel(id=cartId, userId=data["userid"], listItem=cartItems)

    @staticmethod
    async def add_to_cart(cartItem: CartItemCreate):
        conn = await CartService.db.acquire()
        query = f"INSERT INTO {CartItemService.dbCartItem} (quantity, itemid, cartid) values (%s, %s, %s)"
        try:
            cart = await CartService.getByUserId(cartItem.userId)
            if(not cart):
                await CartService.create(CartModel(userId=cartItem.userId))
                cart = await CartService.getByUserId(cartItem.userId)
            cart = cart[0]

            values = (cartItem.quantity, cartItem.itemId, cart.id)
            item = await ItemService.getById(cartItem.itemId)
            if item.quantity < cartItem.quantity:
                raise HTTPException(status_code=400, detail="Insufficient quantity in stock.")

            for it in cart.listItem:
                if(it.item.id == item.id):
                    await CartItemService.changeQuantity(cartItemId=it.id, quantity=cartItem.quantity)
                    return True
            async with conn.cursor() as cursor:
                await cursor.execute(query, values)
                await conn.commit()
            return True
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to create cart item: {str(e)}")
        finally:
            await CartService.db.release(conn)
            
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
            await CartService.db.release(conn)

    @staticmethod
    async def getTotal(cartId: UUID) -> float:
        cartItems: List[CartItemModel] = await CartItemService.getByCartId(cartId)
        total = 0.0
        from app.services.ItemService import ItemService
        for item in cartItems:
            total += item.item.price * item.quantity
        return total
