from django.contrib.auth import authenticate, get_user_model
from django.http import HttpRequest
from django.shortcuts import render
from rest_framework.decorators import action, permission_classes
from rest_framework.views import APIView, Response, status
from rest_framework.viewsets import ViewSet
from water_reminder_api.models import UserAnatomy
from water_reminder_auth.models import UserAuthSession
from water_reminder_auth.permissions import IsAuthenticated

from water_reminder_auth.serializers import UserSerializer, UserSessionSerializer


# Create your views here.
class AuthView(ViewSet):
    @action(detail=False, methods=["post"], url_path="auth", url_name="auth")
    def auth(self, request):
        data = request.data
        username = data["username"]
        password = data["password"]

        user = self._authenticate_user(username, password)
        session = UserAuthSession.create_session(user)

        return Response(UserSessionSerializer(session).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="register", url_name="register")
    def register(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=["get"],
        url_path="me",
        url_name="me",
        permission_classes=[IsAuthenticated],
    )
    def logged_user(self, request):
        user = UserAuthSession.get_auth_user(request)
        user_anatomy = UserAnatomy.objects.filter(user=user).first()
        if not user or not user_anatomy:
            raise Exception("user or his anatomy information not founded")

        return Response(
            UserSerializer(UserAuthSession.get_auth_user(request)).data,
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["post"], url_path="refresh", url_name="refresh")
    def refresh_token(self, request):
        pass

    def _authenticate_user(self, username, password):
        user = authenticate(username=username, password=password)
        if not user:
            raise Exception("error username or password is invalid")

        return user
