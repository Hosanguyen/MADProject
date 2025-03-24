from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

client = AsyncIOMotorClient(settings.MONGO_URI)
db = client["mad"]
statistic_type_collection = db["statistic_type"]
statistic_data_collection = db["statistic_data"]
