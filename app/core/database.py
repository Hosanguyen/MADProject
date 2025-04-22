import aiomysql
from app.core.config import settings

class Database:
    def __init__(self):
        self.pool = None

    async def connect(self):
        self.pool = await aiomysql.create_pool(
            host=settings.MYSQL_HOST,
            port=int(settings.MYSQL_PORT),
            user=settings.MYSQL_USER,
            password=settings.MYSQL_PASSWORD,
            db=settings.MYSQL_DB,
            autocommit=True
        )

    async def disconnect(self):
        if self.pool:
            self.pool.close()
            await self.pool.wait_closed()

    async def acquire(self):
        if not self.pool:
            await self.connect()
        return await self.pool.acquire()
    
    async def release(self, conn):
        if self.pool and conn:
            self.pool.release(conn)

