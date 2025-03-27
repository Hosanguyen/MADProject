from app.models.StatisticDataModel import StatisticDataModel
from uuid import UUID

class StatisticDataCreate(StatisticDataModel):
    petId: UUID
    statisticTypeId : UUID