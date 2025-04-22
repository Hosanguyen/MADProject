from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class OrderCreate(BaseModel):
    id: Optional[UUID] = None
    userId: UUID
