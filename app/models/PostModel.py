from pydantic import BaseModel
from typing import Optional
from app.schemas.UserSchema import UserPost


class PostModel(BaseModel):
    id: Optional[str] = None
    content: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    user_id: Optional[str] = None