from rest_framework import viewsets
from django_filters import rest_framework as filters
from rest_framework.views import Response, status
from water_reminder_api.filters import WaterConsumptionHistoryFilter
from water_reminder_api.models import WaterConsumptionHistory
from water_reminder_api.serializers import WaterConsumptionHistorySerializer
from water_reminder_auth.permissions import IsAuthenticated


# Create your views here.
class WaterConsumptionHistoryView(viewsets.ModelViewSet):
    queryset = WaterConsumptionHistory.objects.all()
    serializer_class = WaterConsumptionHistorySerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = WaterConsumptionHistoryFilter
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        request.data.update({"user": request.user.id})
        return super().create(request, *args, **kwargs)

    # def destroy(self, request, pk=None):
    #     waterConsumptionRecord = WaterConsumptionHistory.objects.filter(id=pk).first()
    #     if not waterConsumptionRecord:
    #         return Response(status=status.HTTP_404_NOT_FOUND)

    #     waterConsumptionRecord.delete()
    #     return Response(
    #         WaterConsumptionHistorySerializer(waterConsumptionRecord).data,
    #         status=status.HTTP_200_OK,
    #     )
