from django.http import HttpResponse
from django.utils import timezone
from rest_framework.views import status
from rest_framework import exceptions
from water_reminder_auth.models import UserAuthSession


class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
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


class CorsMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Headers"] = "*"
        return response
