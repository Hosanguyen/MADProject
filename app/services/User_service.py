import uuid
import bcrypt
from app.models.User import UserRegister, UserResponse, UserLogin, UserSyncPush, UserSyncPull
from app.core.database import Database
from fastapi import HTTPException
import aiomysql

db = Database()
async def register(user: UserRegister):
    if not user.username or not user.hashed_password or not user.fullname:
        raise HTTPException(status_code=400, detail="Thiếu thông tin bắt buộc")

    async with db.acquire() as conn:
        try:
            async with conn.cursor() as cur:
                # Kiểm tra xem username đã tồn tại chưa
                check_user_query = "SELECT id FROM user WHERE username = %s"
                check_user_values = (user.username,)
                await cur.execute(check_user_query, check_user_values)
                existing_user = await cur.fetchone()
                if existing_user:
                    raise HTTPException(status_code=400, detail="Tên người dùng đã tồn tại")

                # Tạo UUID
                user_id = str(uuid.uuid4())

                # Chèn người dùng mới
                insert_user_query = "INSERT INTO user (id, username, password, fullname, image_url) VALUES (%s, %s, %s, %s, %s)"
                insert_user_values = (user_id, user.username, user.hashed_password, user.fullname, user.image_url)
                await cur.execute(insert_user_query, insert_user_values)
                await conn.commit()

                # Trả về thông tin người dùng mới đăng ký
                return UserResponse(
                    id=user_id,
                    username=user.username,
                    fullname=user.fullname,
                    image_url=user.image_url
                )
        except aiomysql.MySQLError as e:
            await conn.rollback()
            raise HTTPException(status_code=500, detail=f"Lỗi cơ sở dữ liệu: {str(e)}")
        except Exception as e:
            await conn.rollback()
            raise HTTPException(status_code=500, detail=f"Lỗi không xác định: {str(e)}")


async def login(user: UserLogin):
    if not user.username or not user.hashed_password:
        raise HTTPException(status_code=400, detail="Thiếu thông tin bắt buộc")

    async with db.acquire() as conn:
        try:
            async with conn.cursor() as cur:
                # Kiểm tra xem username đã tồn tại chưa
                check_user_query = "SELECT id, username, password, fullname, image_url FROM user WHERE username = %s"
                check_user_values = (user.username,)
                await cur.execute(check_user_query, check_user_values)
                existing_user = await cur.fetchone()
                if not existing_user:
                    raise HTTPException(status_code=400, detail="Tên người dùng không tồn tại")

                # Kiểm tra mật khẩu
                if not bcrypt.checkpw(user.hashed_password.encode('utf-8'), existing_user[2].encode('utf-8')):
                    raise HTTPException(status_code=400, detail="Mật khẩu không chính xác")

                # Trả về thông tin người dùng
                return UserResponse(
                    id=existing_user[0],
                    username=existing_user[1],
                    fullname=existing_user[3],
                    image_url=existing_user[4]
                )
        except aiomysql.MySQLError as e:
            raise HTTPException(status_code=500, detail=f"Lỗi cơ sở dữ liệu: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Lỗi không xác định: {str(e)}")


async def push_sync_user(user: UserSyncPush):
    if not user.fullname:
        raise HTTPException(status_code=400, detail="Thiếu thông tin bắt buộc")

    async with db.acquire() as conn:
        try:
            async with conn.cursor() as cur:
                # Kiểm tra xem username đã tồn tại chưa
                check_user_query = "SELECT id FROM user WHERE id = %s"
                check_user_values = (user.id,)
                await cur.execute(check_user_query, check_user_values)
                existing_user = await cur.fetchone()
                if not existing_user:
                    raise HTTPException(status_code=400, detail="Người dùng không tồn tại")

                # Cập nhật thông tin người dùng
                update_user_query = "UPDATE user SET fullname = %s WHERE id = %s"
                update_user_values = (user.fullname, user.id)
                await cur.execute(update_user_query, update_user_values)
                await conn.commit()
        except aiomysql.MySQLError as e:
            await conn.rollback()
            raise HTTPException(status_code=500, detail=f"Lỗi cơ sở dữ liệu: {str(e)}")
        except Exception as e:
            await conn.rollback()
            raise HTTPException(status_code=500, detail=f"Lỗi không xác định: {str(e)}")

    return {"massage": "Sync ok"}


async def pull_sync_user(user: UserSyncPull):
    async with db.acquire() as conn:
        try:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                # Kiểm tra xem username đã tồn tại chưa
                check_user_query = "SELECT id FROM user WHERE id = %s"
                check_user_values = (user.id,)
                await cur.execute(check_user_query, check_user_values)
                existing_user = await cur.fetchone()
                if not existing_user:
                    raise HTTPException(status_code=400, detail="Người dùng không tồn tại")

                # Trả về thông tin người dùng
                return UserResponse(**existing_user)
        except aiomysql.MySQLError as e:
            raise HTTPException(status_code=500, detail=f"Lỗi cơ sở dữ liệu: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Lỗi không xác định: {str(e)}")