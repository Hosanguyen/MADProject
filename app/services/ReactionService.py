from app.core.database import Database
from app.models.ReactionModel import ReactionModel
import aiomysql

class ReactionService:
    db = Database()

    @staticmethod
    async def get_reactions_by_postid(post_id: str):
        conn = await ReactionService.db.acquire()
        query = "SELECT * FROM reaction WHERE postid = %s"
        values = (post_id)
        try:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query, values)
                rows = await cursor.fetchall()
                reactions = []
                for row in rows:
                    reaction = ReactionModel()
                    reaction.id = row['id']
                    reaction.type = row['type']
                    reaction.post_id = row['postid'] or None
                    reaction.user_id = row['userid'] or None
                    reaction.created_at = str(row['created_at']) if row else None
                    reaction.updated_at = str(row['updated_at']) if row else None
                    reactions.append(reaction)
        finally:
            conn.close()
        return reactions
    
    @staticmethod
    async def create_reaction(reaction: ReactionModel):
        conn = await ReactionService.db.acquire()
        query = "INSERT INTO reaction (type, userid, postid) VALUES (%s, %s, %s)"
        try:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query, (reaction.type, reaction.user_id, reaction.post_id))
                await conn.commit()
        finally:
            conn.close()
        return True
    
    @staticmethod
    async def delete_reaction(reaction_id: str):
        conn = await ReactionService.db.acquire()
        query = "DELETE FROM reaction WHERE id = %s"
        values = (reaction_id)
        try:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query, values)
                await conn.commit()
        finally:
            conn.close()
        return True
    
    @staticmethod
    async def update_reaction(reaction: ReactionModel):
        conn = await ReactionService.db.acquire()
        query = "UPDATE reaction SET type = %s WHERE id = %s"
        try:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query, (reaction.type, reaction.id))
                await conn.commit()
        finally:
            conn.close()
        return True
    
    @staticmethod
    async def get_reaction_by_id(reaction_id: str):
        conn = await ReactionService.db.acquire()
        query = "SELECT * FROM reaction WHERE id = %s"
        values = (reaction_id)
        try:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query, values)
                row = await cursor.fetchone()
                if row:
                    reaction = ReactionModel()
                    reaction.id = row['id']
                    reaction.type = row['type']
                    reaction.post_id = row['postid'] or None
                    reaction.user_id = row['userid'] or None
                    reaction.created_at = str(row['created_at']) if row else None
                    reaction.updated_at = str(row['updated_at']) if row else None
                    return reaction
        finally:
            conn.close()
        return None