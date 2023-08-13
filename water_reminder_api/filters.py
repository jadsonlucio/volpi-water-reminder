from django_filters import rest_framework as filters

from water_reminder_api.models import WaterConsumptionHistory


class WaterConsumptionHistoryFilter(filters.FilterSet):
    date = filters.DateFromToRangeFilter()

    class Meta:
        model = WaterConsumptionHistory
        fields = ["date"]
