from app.models.ItemModel import ItemModel
from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from fastapi import UploadFile
class ItemCreate:
    def __init__(
        self,
        name: str,
        quantity: int,
        price: float,
        description: Optional[str],
        manufacturer: str,
        image: Optional[UploadFile],
        itemTypeId: UUID
    ):
        self.name = name
        self.quantity = quantity
        self.price = price
        self.description = description
        self.manufacturer = manufacturer
        self.image = image
        self.itemTypeId = itemTypeId

class ItemUpdate:
    def __init__(
        self,
        id: UUID,
        name: str,
        quantity: int,
        price: float,
        description: Optional[str],
        manufacturer: str,
        image: Optional[UploadFile] = None,
        itemTypeId: UUID = None
    ):
        self.id = id
        self.name = name
        self.quantity = quantity
        self.price = price
        self.description = description
        self.manufacturer = manufacturer
        self.image = image
        self.itemTypeId = itemTypeId

class ItemUpdateQuantity(BaseModel):
    itemId: UUID
    quantity: int

class ItemResponseCart(BaseModel):
    id: UUID
    name: str
    price: float
    description: Optional[str] = None
    manufacturer: str
    