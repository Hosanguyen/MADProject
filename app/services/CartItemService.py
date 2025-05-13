import aiomysql
from typing import List
from fastapi import HTTPException
from uuid import UUID

from app.core.database import Database
from app.models.CartItemModel import CartItemModel
from app.schemas.CartItemSchema import CartItemCreate
from app.services.ItemService import ItemService
from app.schemas.ItemSchema import ItemResponseCart

class CartItemService:
    db = Database()
    dbCartItem = "cart_item"

    @staticmethod
    async def create(cartItem: CartItemCreate) -> bool:
        conn = await CartItemService.db.acquire()
        query = f"INSERT INTO {CartItemService.dbCartItem} (quantity, itemid, cartid) VALUES (%s, %s, %s)"
        values = (cartItem.quantity, cartItem.itemId, cartItem.cartId)
        try:
            item = await ItemService.getById(cartItem.itemId)
            if item.get("quantity") < cartItem.quantity:
                raise HTTPException(status_code=400, detail="Insufficient quantity in stock.")

            async with conn.cursor() as cursor:
                await cursor.execute(query, values)
                await conn.commit()
            return True
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to create cart item: {str(e)}")
        finally:
            await CartItemService.db.release(conn)

    @staticmethod
    async def getAll() -> List[CartItemModel]:
        conn = await CartItemService.db.acquire()
        query = f"SELECT id, quantity, itemid, cartid FROM {CartItemService.dbCartItem}"
        try:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query)
                datas = await cursor.fetchall()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to retrieve cart items: {str(e)}")
        finally:
            await CartItemService.db.release(conn)

        result = []
        for data in datas:
            item = await ItemService.getById(data.get("itemid"))
            itemResponse = ItemResponseCart(id=item.id, name=item.name, price=item.price, description=item.description, manufacturer=item.manufacturer)
            cartItem = CartItemModel(id=data.get("id"), quantity=data.get("quantity"), item=itemResponse)
            result.append(cartItem)
        return result

    @staticmethod
    async def getByCartId(cartId: UUID) -> List[CartItemModel]:
        conn = await CartItemService.db.acquire()
        query = f"SELECT id, quantity, itemid FROM {CartItemService.dbCartItem} WHERE cartid = %s"
        values = (cartId,)
        try:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query, values)
                datas = await cursor.fetchall()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to retrieve cart items by cart ID: {str(e)}")
        finally:
            await CartItemService.db.release(conn)

        result = []
        for data in datas:
            item = await ItemService.getById(data.get("itemid"))
            itemResponse = ItemResponseCart(id=item.id, name=item.name, price=item.price, description=item.description, manufacturer=item.manufacturer, image_url=item.image_url)
            cartItem = CartItemModel(id=data.get("id"), quantity=data.get("quantity"), item=itemResponse)
            result.append(cartItem)
        return result

    @staticmethod
    async def getById(cartItemId: UUID) -> CartItemModel:
        conn = await CartItemService.db.acquire()
        query = f"SELECT id, quantity, itemid, cartid FROM {CartItemService.dbCartItem} WHERE id = %s"
        values = (cartItemId,)
        try:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query, values)
                data = await cursor.fetchone()
                if not data:
                    raise HTTPException(status_code=404, detail="Cart item not found.")
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to retrieve cart item by ID: {str(e)}")
        finally:
            await CartItemService.db.release(conn)

        item = await ItemService.getById(data.get("itemid"))
        itemResponse = ItemResponseCart(id=item.id, name=item.name, price=item.price, description=item.description, manufacturer=item.manufacturer, image_url=item.image_url)
        cartItem = CartItemModel(id=data.get("id"), quantity=data.get("quantity"), item=itemResponse)
        return cartItem

    @staticmethod
    async def changeQuantity(cartItemId: UUID, quantity: int) -> bool:
        conn = await CartItemService.db.acquire()
        
        try:
            query_get_cart_item = f"SELECT itemid, quantity FROM {CartItemService.dbCartItem} WHERE id = %s"
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query_get_cart_item, (cartItemId,))
                cartItem = await cursor.fetchone()
                if not cartItem:
                    raise HTTPException(status_code=404, detail="Cart item not found.")

            current_quantity = cartItem["quantity"]
            item_id = cartItem["itemid"]

            # Lấy thông tin sản phẩm
            item = await ItemService.getById(item_id)
            if not item:
                raise HTTPException(status_code=404, detail="Item not found.")

            item_stock = item.quantity
            new_quantity = current_quantity + quantity
       
            if new_quantity > item_stock:
                raise HTTPException(status_code=400, detail="Insufficient quantity in stock.")

            # Update vào database
            query_update = f"UPDATE {CartItemService.dbCartItem} SET quantity = GREATEST(%s, 0) WHERE id = %s"
            async with conn.cursor() as cursor:
                await cursor.execute(query_update, (new_quantity, cartItemId))
                await conn.commit()
            return True

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to update cart item quantity: {str(e)}")
        finally:
            await CartItemService.db.release(conn)

    @staticmethod
    async def delete(cartItemId: UUID) -> bool:
        conn = await CartItemService.db.acquire()
        query = f"DELETE FROM {CartItemService.dbCartItem} WHERE id = %s"
        values = (cartItemId,)
        try:
            async with conn.cursor() as cursor:
                await cursor.execute(query, values)
                await conn.commit()
                if cursor.rowcount == 0:
                    raise HTTPException(status_code=404, detail="Cart item not found for deletion.")
            return True
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to delete cart item: {str(e)}")
        finally:
            await CartItemService.db.release(conn)

    @staticmethod
    async def remove(cartItemId: UUID) -> bool:
        conn = await CartItemService.db.acquire()
        query = f"UPDATE {CartItemService.dbCartItem} SET cartid = 0 WHERE id = %s"
        values = (cartItemId,)
        try:
            async with conn.cursor() as cursor:
                await cursor.execute(query, values)
                await conn.commit()
                if cursor.rowcount == 0:
                    raise HTTPException(status_code=404, detail="Cart item not found for deletion.")
            return True
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to delete cart item: {str(e)}")
        finally:
            await CartItemService.db.release(conn)