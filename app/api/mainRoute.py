from fastapi import APIRouter
from app.api.routes import statistic, item, itemType
from app.core.config import settings

api_router = APIRouter()
api_router.include_router(statistic.router)
api_router.include_router(itemType.router)
api_router.include_router(item.router)
