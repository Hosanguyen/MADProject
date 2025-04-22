from pydantic import BaseModel
from typing import Optional

class ReactionModel(BaseModel):
    id: Optional[str] = None
    post_id: Optional[str] = None
    user_id: Optional[str] = None
    type: Optional[str] = None  # e.g., 'like', 'love', 'laugh', etc.
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
