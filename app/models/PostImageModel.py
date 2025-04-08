from pydantic import BaseModel
from typing import Optional

class PostImageModel(BaseModel):
    id: Optional[str] = None
    post_id: Optional[str] = None
    image_url: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None



