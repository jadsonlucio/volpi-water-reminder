from django.contrib import admin
from water_reminder_api.models import UserAnatomy, WaterConsumptionHistory


# Register your models here.
class WaterConsumptionAdmin(admin.ModelAdmin):
    pass


class UserAttributesAdmin(admin.ModelAdmin):
    pass


admin.site.register(WaterConsumptionHistory, WaterConsumptionAdmin)
admin.site.register(UserAnatomy)
