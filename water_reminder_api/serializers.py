from rest_framework import serializers

from water_reminder_api.models import WaterConsumptionHistory


class WaterConsumptionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WaterConsumptionHistory
        fields = ["date", "consumption_ml", "user", "id"]
        read_only_fields = ["id"]
        extra_kwargs = {"user": {"write_only": True}}
