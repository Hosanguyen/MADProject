import uuid
import bcrypt
from app.models.User import (
    UserRegister,
    UserResponse,
    UserLogin,
    UserSyncPush,
    UserSyncPull,
)
from app.core.database import Database
from fastapi import HTTPException
import aiomysql
from typing import Dict, Any, Optional
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

db = Database()


async def _get_user_by_field(field: str, value: str) -> Optional[Dict[str, Any]]:
    """
    Helper function to get a user by a specific field.

    Args:
        field: The database field to search by (e.g., "id", "username")
        value: The value to search for

    Returns:
        User data dictionary or None if not found
    """
    conn = await db.acquire()
    try:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            query = f"SELECT id, username, password, fullname, image_url FROM user WHERE {field} = %s"
            await cur.execute(query, (value,))
            return await cur.fetchone()
    except Exception as e:
        logger.error(f"Database error in _get_user_by_field: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        await db.release(conn)


async def register(user: UserRegister) -> UserResponse:
    """
    Register a new user.

    Args:
        user: User registration data

    Returns:
        UserResponse object with the new user's data

    Raises:
        HTTPException: If required fields are missing, username exists, or database error occurs
    """
    if not user.username or not user.password or not user.fullname:
        raise HTTPException(status_code=400, detail="Thiếu thông tin bắt buộc")

    conn = await db.acquire()
    try:
        async with conn.cursor() as cur:
            # Check if username already exists
            existing_user = await _get_user_by_field("username", user.username)
            if existing_user:
                raise HTTPException(status_code=400, detail="Tên người dùng đã tồn tại")

            # Create a new UUID
            user_id = user.id
            # Hash the password
            hashed_password = bcrypt.hashpw(
                user.password.encode("utf-8"), bcrypt.gensalt()
            ).decode("utf-8")

            # Insert new user
            insert_user_query = """
                INSERT INTO user (id, username, password, fullname, image_url) 
                VALUES (%s, %s, %s, %s, %s)
            """
            insert_user_values = (
                user_id,
                user.username,
                hashed_password,
                user.fullname,
                user.image_url,
            )
            await cur.execute(insert_user_query, insert_user_values)
            await conn.commit()

            # Return new user info
            return UserResponse(
                id=user_id,
                username=user.username,
                fullname=user.fullname,
                image_url=user.image_url,
            )
    except Exception as e:
        logger.error(f"Error in register: {str(e)}")


async def login(user: UserLogin) -> UserResponse:
    """
    Log in a user.

    Args:
        user: User login credentials

    Returns:
        UserResponse object with the user's data

    Raises:
        HTTPException: If required fields are missing, user doesn't exist, password is incorrect, or database error occurs
    """
    if not user.username or not user.password:
        raise HTTPException(status_code=400, detail="Thiếu thông tin đăng nhập")

    try:
        # Get user by username
        existing_user = await _get_user_by_field("username", user.username)
        if not existing_user:
            raise HTTPException(status_code=401, detail="Tên người dùng không tồn tại")

        # Check password
        stored_password = existing_user["password"]
        if not bcrypt.checkpw(
            user.password.encode("utf-8"), stored_password.encode("utf-8")
        ):
            raise HTTPException(status_code=401, detail="Mật khẩu không chính xác")

        # Return user data
        return UserResponse(
            id=existing_user["id"],
            username=existing_user["username"],
            fullname=existing_user["fullname"],
            image_url=existing_user["image_url"],
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in login: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Lỗi đăng nhập: {str(e)}")


async def push_sync_user(user: UserSyncPush) -> Dict[str, str]:
    """
    Sync user data from client to server.

    Args:
        user: User data to sync

    Returns:
        Success message

    Raises:
        HTTPException: If required fields are missing, user doesn't exist, or database error occurs
    """
    if not user.id or not user.fullname:
        raise HTTPException(status_code=400, detail="Thiếu thông tin bắt buộc")

    conn = await db.acquire()
    try:
        async with conn.cursor() as cur:
            # Check if user exists
            existing_user = await _get_user_by_field("id", user.id)
            if not existing_user:
                raise HTTPException(status_code=404, detail="Người dùng không tồn tại")

            # Update user information
            update_user_query = """
                UPDATE user 
                SET fullname = %s, image_url = %s 
                WHERE id = %s
            """
            update_user_values = (user.fullname, user.image_url, user.id)
            await cur.execute(update_user_query, update_user_values)
            await conn.commit()

            return {"message": "Sync thành công"}
    except aiomysql.MySQLError as e:
        await conn.rollback()
        logger.error(f"MySQL error in push_sync_user: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Lỗi cơ sở dữ liệu: {str(e)}")
    except Exception as e:
        await conn.rollback()
        logger.error(f"Unexpected error in push_sync_user: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Lỗi không xác định: {str(e)}")
    finally:
        await db.release(conn)


async def pull_sync_user(user: UserSyncPull) -> UserResponse:
    """
    Pull user data from server to client.

    Args:
        user: User ID to pull data for

    Returns:
        UserResponse object with the user's data

    Raises:
        HTTPException: If user doesn't exist or database error occurs
    """
    try:
        # Get user by ID
        existing_user = await _get_user_by_field("id", user.id)
        if not existing_user:
            raise HTTPException(status_code=404, detail="Người dùng không tồn tại")

        # Return user data
        return UserResponse(
            id=existing_user["id"],
            username=existing_user["username"],
            fullname=existing_user["fullname"],
            image_url=existing_user["image_url"],
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in pull_sync_user: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Lỗi không xác định: {str(e)}")


async def get_user_by_id(user_id: str) -> UserResponse:
    """
    Get user by ID.

    Args:
        user_id: User ID

    Returns:
        UserResponse object with the user's data

    Raises:
        HTTPException: If user doesn't exist or database error occurs
    """
    try:
        # Get user by ID
        existing_user = await _get_user_by_field("id", user_id)
        if not existing_user:
            raise HTTPException(status_code=404, detail="Người dùng không tồn tại")

        # Return user data
        return UserResponse(
            id=existing_user["id"],
            username=existing_user["username"],
            fullname=existing_user["fullname"],
            image_url=existing_user["image_url"],
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_user_by_id: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Lỗi không xác định: {str(e)}")
