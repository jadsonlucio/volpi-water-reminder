from typing import List, Dict
from itertools import groupby
from functools import reduce
from datetime import datetime

from water_reminder_api.types.WaterConsumptionTypes import (
    DailyWaterConsumptionHistory,
    ConsumptionStatistics,
    WaterConsumptionRecord,
    DailyConsumption,
    DailyWaterConsumptionFilter,
)
from water_reminder_api.models import UserAnatomy, WaterConsumptionHistory
from water_reminder_api.filters import WaterConsumptionHistoryFilter
from water_reminder_api.serializers import WaterConsumptionHistorySerializer

WEIGHT_DAILY_GOAL_FACTOR = 35


def get_daily_goal_consumption(userId: str):
    userAnatomy = UserAnatomy.objects.filter(user__id=userId).first()
    if userAnatomy == None:
        raise Exception(f"user anatomy for user with id: {userId} not found")

    return userAnatomy.weight * WEIGHT_DAILY_GOAL_FACTOR


def get_water_consumption_statistics(
    daily_goal_consumption: float,
    water_consumption_records: List[WaterConsumptionRecord],
) -> ConsumptionStatistics:
    total_consumption_ml = reduce(
        lambda consumption, water_consumption_record: water_consumption_record[
            "consumption_ml"
        ]
        + consumption,
        water_consumption_records,
        0.0,
    )
    return {
        "goal_ml": daily_goal_consumption,
        "percentage_consumption": total_consumption_ml / daily_goal_consumption,
        "total_consumption_ml": total_consumption_ml,
    }


def get_user_daily_water_consumption_history(
    userId: str, filter: DailyWaterConsumptionFilter
) -> DailyWaterConsumptionHistory:
    daily_goal_consumption = get_daily_goal_consumption(userId)
    daily_consumptions: List[DailyConsumption] = []
    water_consumption_records = WaterConsumptionHistoryFilter(
        {"date_before": filter["date_before"], "date_after": filter["date_after"]},
        WaterConsumptionHistory.objects.all(),
    ).qs
    for date, daily_consumption_records in groupby(
        water_consumption_records.iterator(),
        lambda water_consumption_record: str(water_consumption_record.date.date()),
    ):
        daily_consumption_records_serialized: List[WaterConsumptionRecord] = WaterConsumptionHistorySerializer(daily_consumption_records, many=True).data  # type: ignore
        daily_consumption_statistics = get_water_consumption_statistics(
            daily_goal_consumption, daily_consumption_records_serialized
        )
        goal_ml = daily_consumption_statistics["goal_ml"]
        consumption_ml = daily_consumption_statistics["total_consumption_ml"]
        remaining_goal = 0

        if goal_ml > consumption_ml:
            remaining_goal = goal_ml - consumption_ml

        daily_consumptions.append(
            {
                "total_consumption_ml": consumption_ml,
                "date": date,
                "goal_ml": goal_ml,
                "remaining_goal": remaining_goal,
                "percentage_consumption": daily_consumption_statistics[
                    "percentage_consumption"
                ],
                "records": daily_consumption_records_serialized,
            }
        )

    return {"daily_consumptions": daily_consumptions}
