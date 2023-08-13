from django.urls import include, path
from rest_framework import routers
from water_reminder_auth.views import AuthView
from water_reminder_api.views import WaterConsumptionHistoryView

router = routers.DefaultRouter()
router.register("consumption", WaterConsumptionHistoryView)
router.register("", AuthView, "auth")

urlpatterns = [
    path("", include(router.urls), name="api"),
]
