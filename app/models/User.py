from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime, date
from .PetModel import PetBase


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
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserUpdate(UserBase):
    password: Optional[str] = None
    fullname: Optional[str] = None


class UserProfile(UserBase):
    # Relationships
    # pets: List["Pet"] = []
    # posts: List["Post"] = []
    pass

class UserHome(UserBase):
    # Relationships
    pets: List["PetBase"] = []
    # posts: List["Post"] = []
    pass
