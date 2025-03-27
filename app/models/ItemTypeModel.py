from pydantic import BaseModel, Field
from typing import Optional, List
from app.models.ItemModel import ItemModel
from uuid import UUID

class ItemTypeModel(BaseModel):
    id: Optional[UUID] = None
    name: str
    unit: str
    note: Optional[str] = None
    listItem: List[ItemModel] = Field(default_factory=list)