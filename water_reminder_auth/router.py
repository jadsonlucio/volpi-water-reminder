from rest_framework import routers
from water_reminder_auth.views import AuthView

auth_router = routers.DefaultRouter()
auth_router.register(r'', AuthView)