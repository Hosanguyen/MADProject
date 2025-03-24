from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from bson import ObjectId
from app.helpers.PyObjectId import PyObjectId

class StatisticTypeModel(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    name: str = Field(..., description="Tên loại thống kê")
    description: Optional[str] = Field(None, description="Mô tả loại thống kê")
    unit: str = Field(..., description="Đơn vị đo lường")

class StatisticDataModel(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    statistic_type_id: PyObjectId = Field(..., description="ID của loại thống kê")
    value: float = Field(..., description="Giá trị đo được")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Thời gian thu thập dữ liệu")
