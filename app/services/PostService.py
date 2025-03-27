from app.core.database import Database
from app.models.PostModel import PostModel
import aiomysql
from typing import List

class PostService:
    db  = Database()

    @staticmethod
    async def getAll() -> List[PostModel]:
        conn = await PostService.db.acquire()
        query = "SELECT id, content FROM post"
        try:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query)
                posts = await cursor.fetchall()
        finally:
            conn.close()
        return [PostModel(**post) for post in posts]
    
    @staticmethod
    async def create_post(post: PostModel) -> PostModel:
        conn = await PostService.db.acquire()
        query = "INSERT INTO post (content) VALUES (%s)"
        query2 = "SELECT * FROM post where content = %s order by created_at desc limit 1"
        try:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query, (post.content))
                await conn.commit()
                await cursor.execute("SELECT * FROM post WHERE content = %s ORDER BY created_at DESC LIMIT 1", (post.content,))
                row = await cursor.fetchone()
                post.id = row['id'] if row else None
                print(row["created_at"])
                post.created_at = str(row['created_at']) if row else None
                post.updated_at = str(row['updated_at']) if row else None
        finally:
            conn.close()
        return post

