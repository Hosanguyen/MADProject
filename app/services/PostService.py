from app.core.database import Database
from app.models.PostModel import PostModel
from app.models.PostImageModel import PostImageModel
import aiomysql
from typing import List

class PostService:
    db  = Database()

    @staticmethod
    async def getAll() -> List[PostModel]:
        conn = await PostService.db.acquire()
        query = "SELECT * FROM post"
        try:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query)
                posts = await cursor.fetchall()
        finally:
            conn.close()
        kq = []
        for row in posts:
            post = PostModel()
            post.id = str(row['id'])
            post.content = row['content']
            post.created_at = str(row['created_at']) if row else None
            post.updated_at = str(row['updated_at']) if row else None
            kq.append(post)
        return kq
    
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
    
    @staticmethod
    async def get_post_by_id(post_id: str):
        conn = await PostService.db.acquire()
        query = "SELECT * FROM post WHERE id = %s"
        query2 = "SELECT * FROM post_image where postid = %s"
        values = (post_id)
        try:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query, values)
                row = await cursor.fetchone()

                await cursor.execute(query2, values)
                post_images = await cursor.fetchall()
                if row:
                    post = PostModel()
                    post.id = str(row['id'])
                    post.content = row['content']
                    post.created_at = str(row['created_at']) if row else None
                    post.updated_at = str(row['updated_at']) if row else None

                    for image in post_images:
                        post_image = PostImageModel()
                        post_image.id = str(image['id'])
                        post_image.post_id = str(image['postid'])
                        post_image.image_url = image['image_url']
                        post_image.created_at = str(image['created_at']) if row else None
                        post_image.updated_at = str(image['updated_at']) if row else None
                        # Add the image to the post's images list
                        post.images.append(post_image)
                    # post.post_images = [PostImageModel(**image) for image in post_images]
                    return post
        finally:
            conn.close()
        return PostModel(**row) if row else None


    @staticmethod
    async def update_post(post: PostModel):
        conn = await PostService.db.acquire()
        query = "UPDATE post SET content = %s WHERE id = %s"
        values = (post.content, post.id)
        try:
            async with conn.cursor() as cursor:
                await cursor.execute(query, values)
                newPost = await PostService.get_post_by_id(post.id)
                await conn.commit()
        finally:
            conn.close()
        return newPost
    
    @staticmethod
    async def delete_post(post_id: str):
        conn = await PostService.db.acquire()
        query = "DELETE FROM post WHERE id = %s"
        values = (post_id)
        try:
            async with conn.cursor() as cursor:
                await cursor.execute(query, values)
                await conn.commit()
        finally:
            conn.close()
        return True
