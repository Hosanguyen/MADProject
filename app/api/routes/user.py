from fastapi import APIRouter
from app.models.User import UserRegister, UserLogin, UserSyncPush, UserSyncPull
from app.services import User_service

router = APIRouter(tags=["user"])

@router.post("/user/register")
async def register(user: UserRegister):
    return await User_service.register(user)


@router.post("/user/login")
async def login(user: UserLogin):
    return await User_service.login(user)


@router.post("/user/syncPush")
async def sync_push(user: UserSyncPush):
    return await User_service.push_sync_user(user)


@router.post("/user/syncPull")
async def sync_pull(user: UserSyncPull):
    return await User_service.pull_sync_user(user)
