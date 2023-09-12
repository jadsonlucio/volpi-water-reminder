from typing import TypedDict, List, Dict


class ConsumptionStatistics(TypedDict):
    total_consumption_ml: float
    percentage_consumption: float
    goal_ml: float


class WaterConsumptionRecord(TypedDict):
    datetime: str
    consumption_ml: float
    id: int


class DailyConsumption(TypedDict):
    date: str
    total_consumption_ml: float
    percentage_consumption: float
    goal_ml: float
    remaining_goal: float
    records: List[WaterConsumptionRecord]

class DailyWaterConsumptionHistory(TypedDict):
    daily_consumptions: List[DailyConsumption]

class DailyWaterConsumptionFilter(TypedDict):
    date_before: str
    date_after: str
