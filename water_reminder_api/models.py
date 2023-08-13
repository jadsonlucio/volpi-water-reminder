from django.db import models
from django.contrib.auth import get_user_model


class UserAnatomy(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, unique=True)
    weight = models.FloatField()


# Create your models here.
class WaterConsumptionHistory(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    date = models.DateTimeField()
    comsumption_ml = models.FloatField()


class WaterConsumptionDaily(models.Model):
    pass
