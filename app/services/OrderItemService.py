import aiomysql
from typing import List
from fastapi import HTTPException
from uuid import UUID

from app.core.database import Database
from app.models.OrderItemModel import OrderItemModel
from app.schemas.OrderItemSchema import OrderItemCreate
from app.services.CartItemService import CartItemService

class OrderItemService:
    db = Database()
    dbOrderItem = "order_item"

    @staticmethod
    async def create(orderItem: OrderItemCreate) -> bool:
        conn = await OrderItemService.db.acquire()
        query = f"INSERT INTO {OrderItemService.dbOrderItem} (quantity, orderid, cart_itemid) VALUES (%s, %s, %s)"
        try:
            item = await CartItemService.getById(orderItem.cartItemId)
            values = (item.quantity, orderItem.orderId, orderItem.cartItemId)
            async with conn.cursor() as cursor:
                await cursor.execute(query, values)
                await conn.commit()
            return True
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to create order item: {str(e)}")
        finally:
            await conn.ensure_closed()

    @staticmethod
    async def getAll() -> List[OrderItemModel]:
        conn = await OrderItemService.db.acquire()
        query = f"SELECT id, cart_itemid FROM {OrderItemService.dbOrderItem}"
        try:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query)
                datas = await cursor.fetchall()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to retrieve order items: {str(e)}")
        finally:
            await conn.ensure_closed()

        result = []
        for data in datas:
            cartItem = await CartItemService.getById(data.get("cart_itemid"))
            orderItem = OrderItemModel(id=data.get("id"), cartItem=cartItem)
            result.append(orderItem)
        return result

    @staticmethod
    async def getByOrderId(orderId: UUID) -> List[OrderItemModel]:
        conn = await OrderItemService.db.acquire()
        query = f"SELECT id, cart_itemid FROM {OrderItemService.dbOrderItem} WHERE orderid = %s"
        values = (orderId)
        try:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query, values)
                datas = await cursor.fetchall()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to retrieve order items: {str(e)}")
        finally:
            await conn.ensure_closed()

        result = []
        for data in datas:
            cartItem = await CartItemService.getById(data.get("cart_itemid"))
            orderItem = OrderItemModel(id=data.get("id"), cartItem=cartItem)
            result.append(orderItem)
        return result

    @staticmethod
    async def getById(orderItemId: UUID) -> OrderItemModel:
        conn = await OrderItemService.db.acquire()
        query = f"SELECT cart_itemid FROM {OrderItemService.dbOrderItem} WHERE id = %s"
        values = (orderItemId)
        try:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query, values)
                data = await cursor.fetchone()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to retrieve order items: {str(e)}")
        finally:
            await conn.ensure_closed()

        cartItem = await CartItemService.getById(data.get("cart_itemid"))
        orderItem = OrderItemModel(id=orderItemId, cartItem=cartItem)
        return orderItem

    # @staticmethod
    # async def changeQuantity(cartItemId: UUID, quantity: int) -> bool:
    #     conn = await CartItemService.db.acquire()
        
    #     try:
    #         query_get_cart_item = f"SELECT itemid, quantity FROM {CartItemService.dbCartItem} WHERE id = %s"
    #         async with conn.cursor(aiomysql.DictCursor) as cursor:
    #             await cursor.execute(query_get_cart_item, (cartItemId,))
    #             cartItem = await cursor.fetchone()
    #             if not cartItem:
    #                 raise HTTPException(status_code=404, detail="Cart item not found.")

    #         current_quantity = cartItem["quantity"]
    #         item_id = cartItem["itemid"]

    #         # Lấy thông tin sản phẩm
    #         item = await ItemService.getById(item_id)
    #         if not item:
    #             raise HTTPException(status_code=404, detail="Item not found.")

    #         item_stock = item.quantity
    #         new_quantity = current_quantity + quantity
       
    #         if new_quantity > item_stock:
    #             raise HTTPException(status_code=400, detail="Insufficient quantity in stock.")

    #         # Update vào database
    #         query_update = f"UPDATE {CartItemService.dbCartItem} SET quantity = GREATEST(%s, 0) WHERE id = %s"
    #         async with conn.cursor() as cursor:
    #             await cursor.execute(query_update, (new_quantity, cartItemId))
    #             await conn.commit()
    #         return True

    #     except HTTPException:
    #         raise
    #     except Exception as e:
    #         raise HTTPException(status_code=500, detail=f"Failed to update cart item quantity: {str(e)}")
    #     finally:
    #         await conn.ensure_closed()

    @staticmethod
    async def delete(orderItemId: UUID) -> bool:
        conn = await OrderItemService.db.acquire()
        query = f"DELETE FROM {OrderItemService.dbOrderItem} WHERE id = %s"
        values = (orderItemId)
        try:
            async with conn.cursor() as cursor:
                await cursor.execute(query, values)
                await conn.commit()
                if cursor.rowcount == 0:
                    raise HTTPException(status_code=404, detail="Order item not found for deletion.")
            return True
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to delete order item: {str(e)}")
        finally:
            await conn.ensure_closed()
