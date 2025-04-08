from pydantic import BaseModel
from typing import Optional

class CommentModel(BaseModel):
    id: Optional[str] = None
    post_id: Optional[str] = None
    user_id: Optional[str] = None
    content: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
