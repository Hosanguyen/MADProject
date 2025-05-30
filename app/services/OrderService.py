import aiomysql
from typing import List
from fastapi import HTTPException
import uuid
from uuid import UUID

from app.core.database import Database
from app.models.OrderModel import OrderModel
from app.schemas.OrderSchema import OrderCreate
from app.services.OrderItemService import OrderItemService
from app.models.User import UserBase
from app.models.OrderItemModel import OrderItemModel
from app.schemas.OrderSchema import OrderInit
class OrderService:
    db = Database()
    dbOrder = "order"

    @staticmethod
    async def create(orderItem: OrderCreate) -> bool:
        conn = await OrderService.db.acquire()
        query = f"INSERT INTO `{OrderService.dbOrder}` (userid) VALUES (%s)"
        values = (orderItem.userId)
        try:
            async with conn.cursor() as cursor:
                await cursor.execute(query, values)
                await conn.commit()
            return True
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to create order: {str(e)}")
        finally:
            await OrderService.db.release(conn)

    @staticmethod
    async def getAll() -> List[OrderModel]:
        conn = await OrderService.db.acquire()
        query = f"SELECT id, userid FROM `{OrderService.dbOrder}`"
        try:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query)
                datas = await cursor.fetchall()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to retrieve order items: {str(e)}")
        finally:
            await OrderService.db.release(conn)

        result = []
        for data in datas:
            user = await OrderService.getUser(data.get("userid"))
            listOrderItem = await OrderItemService.getByOrderId(data.get("id"))
            order = OrderModel(id=data.get("id"), listOrderItem=listOrderItem, user=user)
            result.append(order)
        return result

    @staticmethod
    async def getByUserId(userId: UUID) -> List[OrderModel]:
        conn = await OrderService.db.acquire()
        query = f"SELECT id FROM `{OrderService.dbOrder}` WHERE userid = %s"
        values = (userId)
        try:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query, values)
                datas = await cursor.fetchall()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to retrieve order items: {str(e)}")
        finally:
            await OrderService.db.release(conn)

        result = []
        for data in datas:
            user = await OrderService.getUser(userId)
            listOrderItem = await OrderItemService.getByOrderId(data.get("id"))
            order = OrderModel(id=data.get("id"), listOrderItem=listOrderItem, user=user)
            result.append(order)
        return result

    @staticmethod
    async def getById(orderId: UUID) -> OrderModel:
        conn = await OrderService.db.acquire()
        query = f"SELECT userid FROM `{OrderService.dbOrder}` WHERE id = %s"
        values = (orderId)
        try:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query, values)
                data = await cursor.fetchone()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to retrieve order items: {str(e)}")
        finally:
            await OrderService.db.release(conn)

        user = await OrderService.getUser(data.get("userid"))
        listOrderItem = await OrderItemService.getByOrderId(orderId)
        order = OrderModel(id=orderId, listOrderItem=listOrderItem, user=user)
        return order

    @staticmethod
    async def delete(orderId: UUID) -> bool:
        conn = await OrderService.db.acquire()
        query = f"DELETE FROM `{OrderService.dbOrder}` WHERE id = %s"
        values = (orderId)
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
            await OrderService.db.release(conn)

    @staticmethod
    async def getUser(userId: UUID):
        conn = await OrderService.db.acquire()
        query = f"SELECT fullname, image_url FROM user WHERE id = %s"
        values = (userId)
        try:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query, values)
                userData = await cursor.fetchone()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to retrieve user: {str(e)}")
        finally:
            await OrderService.db.release(conn)
        user = UserBase(fullname=userData.get("fullname"), image_url=userData.get("image_url"))
        return user
    
    @staticmethod
    async def createOrder(order: OrderInit):
        if not order:
            raise HTTPException(status_code=400, detail="Order item list is empty.")
        
        userId = order.userId
        orderId = uuid.uuid4()
        conn = await OrderService.db.acquire()
        try:
            async with conn.cursor(aiomysql.DictCursor) as cursor:

                for item in order.listItem:
                    cartItemId = item.cartItem.id
                    quantityRequested = item.cartItem.quantity

                    # Lấy thông tin sản phẩm tương ứng từ cart_item
                    await cursor.execute("""
                        SELECT itemid FROM cart_item WHERE id = %s
                    """, (cartItemId,))
                    cartItem = await cursor.fetchone()
                    if not cartItem:
                        raise HTTPException(status_code=404, detail=f"Cart item {cartItemId} not found.")
                    
                    productId = cartItem['itemid']
                    await cursor.execute("""
                        SELECT quantity FROM item WHERE id = %s
                    """, (productId,))
                    product = await cursor.fetchone()
                    if not product:
                        raise HTTPException(status_code=404, detail=f"Product {productId} not found.")
                
                    if product['quantity'] < quantityRequested:
                        raise HTTPException(
                            status_code=400,
                            detail=f"Product {productId} does not have enough stock. Available: {product['quantity']}, requested: {quantityRequested}"
                        )
                    
                order_query = f"INSERT INTO `{OrderService.dbOrder}` (id, userid) VALUES (%s, %s)"
                order_query_values = (str(orderId), str(userId))
                await cursor.execute(order_query, order_query_values)

                item_query = """
                    INSERT INTO order_item (quantity, orderid, cart_itemid)
                    VALUES (%s, %s, %s)
                """
                for item in order.listItem:
                    values = (item.cartItem.quantity, orderId, item.cartItem.id)
                    await cursor.execute(item_query, values)
                    await cursor.execute("""
                        UPDATE item
                        SET quantity = quantity - %s
                        WHERE id = (
                            SELECT itemid FROM cart_item WHERE id = %s
                        )
                    """, (item.cartItem.quantity, item.cartItem.id))
                await conn.commit()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to retrieve user: {str(e)}")
        finally:
            await OrderService.db.release(conn)
    