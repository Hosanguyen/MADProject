from app.models.User import UserBase
from typing import Optional
from pydantic import BaseModel

class UserPost(BaseModel):
    fullname: str
    image_url: Optional[str] = None