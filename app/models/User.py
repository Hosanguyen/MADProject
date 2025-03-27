from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime, date


class UserBase(BaseModel):
    # id: Optional[int] = None
    # username: str
    # password: str
    fullname: str
    image_url: Optional[str] = None
    # Relationships
    # pets: List["Pet"] = []
    # posts: List["Post"] = []
    # comments: List["Comment"] = []
    # reactions: List["Reaction"] = []
    # carts: List["Cart"] = []
    # orders: List["Order"] = []


class UserRegister(UserBase):
    username: str
    hashed_password: str

class UserResponse(UserBase):
    id: str
    username: str


class UserLogin(BaseModel):
    username: str
    hashed_password: str


class UserUpdate(UserBase):
    password: Optional[str] = None
    fullname: Optional[str] = None


class UserSyncPush(UserBase):
    fullname: str = None
    image_base64: str = None
    created_at: datetime
    updated_at: datetime


class UserSyncPull(UserBase):
    id: str
    username: str
    image_base64: str = None
    created_at: datetime
    updated_at: datetime



