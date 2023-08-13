from django.forms.utils import timezone
from rest_framework import authentication, exceptions

from water_reminder_auth.models import UserAuthSession


class WaterReminderAuthenticator(authentication.BaseAuthentication):
    def authenticate(self, request):
        if UserAuthSession.AUTH_TOKEN_NAME in request.headers:
            auth_token = request.headers[UserAuthSession.AUTH_TOKEN_NAME]
            user_auth_session = UserAuthSession.objects.filter(
                auth_token=auth_token
            ).first()
            if not user_auth_session:
                raise exceptions.AuthenticationFailed("User not found")
            if timezone.now() > user_auth_session.expiration_datetime:
                raise exceptions.AuthenticationFailed("token expired")

            return (user_auth_session.user, None)

        return None
