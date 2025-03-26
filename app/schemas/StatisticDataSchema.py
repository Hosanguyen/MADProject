from app.models.StatisticDataModel import StatisticDataModel

class StatisticDataCreate(StatisticDataModel):
    petId: int
    statisticTypeId : int