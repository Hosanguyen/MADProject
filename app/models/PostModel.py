from pydantic import BaseModel
from typing import Optional
from app.schemas.UserSchema import UserPost
from app.models.PostImageModel import PostImageModel


class PostModel(BaseModel):
    id: Optional[str] = None
    content: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    user_id: Optional[str] = None
    images: Optional[list[PostImageModel]] = None  # List of image URLs