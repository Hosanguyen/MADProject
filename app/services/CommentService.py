from app.core.database import Database
from app.models.CommentModel import CommentModel
import aiomysql

class CommentService:
    db = Database()

    @staticmethod
    async def get_comments_post(post_id: str):
        conn = await CommentService.db.acquire()
        query = "SELECT * FROM comment WHERE postid = %s"
        values = (post_id)
        try:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query, values)
                rows = await cursor.fetchall()
                comments = []
                for row in rows:
                    comment = CommentModel()
                    comment.id = row['id']
                    comment.content = row['content']
                    comment.user_id = row['userid']
                    comment.post_id = row['postid']
                    comment.created_at = str(row['created_at']) if row else None
                    comment.updated_at = str(row['updated_at']) if row else None
                    comments.append(comment)

        finally:
            conn.close()
        return comments
    
    @staticmethod
    async def create_comment(comment: CommentModel):
        conn = await CommentService.db.acquire()
        query = "INSERT INTO comment (content, userid, postid) VALUES (%s, %s, %s)"
        try:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query, (comment.content, comment.user_id, comment.post_id))
                await conn.commit()
        finally:
            conn.close()
        return True
    
    @staticmethod
    async def delete_comment(comment_id: str):
        conn = await CommentService.db.acquire()
        query = "DELETE FROM comment WHERE id = %s"
        values = (comment_id)
        try:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query, values)
                await conn.commit()
        finally:
            conn.close()
        return True
    
    @staticmethod
    async def update_comment(comment: CommentModel):
        conn = await CommentService.db.acquire()
        query = "UPDATE comment SET content = %s WHERE id = %s"
        values = (comment.content, comment.id)
        try:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query, values)
                await conn.commit()
        finally:
            conn.close()
        return True
    
    @staticmethod
    async def get_comment_by_id(comment_id: str):
        conn = await CommentService.db.acquire()
        query = "SELECT * FROM comment WHERE id = %s"
        values = (comment_id)
        try:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query, values)
                row = await cursor.fetchone()
                if row:
                    comment = CommentModel()
                    comment.id = row['id']
                    comment.content = row['content']
                    comment.user_id = row['userid'] or None
                    comment.post_id = row['postid'] or None
                    comment.created_at = str(row['created_at']) if row else None
                    comment.updated_at = str(row['updated_at']) if row else None
                    return comment
        finally:
            conn.close()
        return None

    @staticmethod
    async def get_total_comments_post(post_id:str):
        conn = await CommentService.db.acquire()
        query = "SELECT COUNT(id) FROM comment WHERE postid = %s"
        values = (post_id)
        try:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query, values)
                row = await cursor.fetchone()
                if row:
                    return row['COUNT(id)']
        finally:
            conn.close()
        return 0

    