from datetime import datetime, timedelta
from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from uuid import uuid4


# Create your models here.
class UserAuthSession(models.Model):
    AUTH_TOKEN_NAME = "Authorization"

    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, unique=True)
    auth_token = models.CharField(unique=True, max_length=255)
    refresh_token = models.CharField(unique=True, max_length=255)
    expiration_datetime = models.DateTimeField()

    def is_expired(self):
        return self.expiration_datetime >= datetime.now()

    def refresh(self):
        pass

    @classmethod
    def create_session(cls, user):
        user_session = UserAuthSession.objects.filter(user=user).first()
        if user_session:
            user_session.delete()

        auth_token = uuid4()
        refresh_token = uuid4()
        current_datetime = datetime.now()
        token_duration_minutes = settings.TOKEN_DURATION_MINUTES or 1440
        expiration_datetime = current_datetime + timedelta(
            minutes=token_duration_minutes
        )
        user_auth_session = cls(
            user=user,
            auth_token=auth_token,
            refresh_token=refresh_token,
            expiration_datetime=expiration_datetime,
        )
        user_auth_session.save()

        return user_auth_session

    @classmethod
    def get_auth_user(cls, request):
        if cls.AUTH_TOKEN_NAME not in request.headers:
            raise Exception("auth token must be on headers")
        auth_token = request.headers[cls.AUTH_TOKEN_NAME]
        if not auth_token:
            raise Exception("auth token not found on request headers")

        user_auth_session = UserAuthSession.objects.filter(
            auth_token=auth_token
        ).first()
        if not user_auth_session:
            raise Exception("user not logged")

        return user_auth_session.user
