import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "water_reminder.settings")
from collections import namedtuple
from datetime import datetime, timedelta
from unittest.mock import Mock
from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.test import TestCase
from rest_framework.views import PermissionDenied, View, status
from water_reminder_auth.middleware import AuthMiddleware

from water_reminder_auth.models import UserAuthSession
from water_reminder_auth.permissions import IsAuthenticated


# Create your tests here.
class AuthTests(TestCase):
    def setUp(self):
        self.first_user = get_user_model().objects.create(
            username="jadson", password="qwer1234", email="test@email.com"
        )
        self.second_user = get_user_model().objects.create(
            username="jadson2", password="qwer1234", email="test2@email.com"
        )

    def test_create_session(self):
        auth_user_session = UserAuthSession.create_session(self.first_user)
        self.assertEqual(auth_user_session.user, self.first_user)
        self.assertIsNotNone(auth_user_session.auth_token)
        self.assertIsNotNone(auth_user_session.refresh_token)
        self.assertIsNotNone(auth_user_session.expiration_datetime)
        auth_user_session_model = UserAuthSession.objects.filter(
            user=self.first_user
        ).first()
        self.assertIsNotNone(auth_user_session_model)

    def test_should_create_new_session_if_already_exist(self):
        auth_user_session_old = UserAuthSession.create_session(self.first_user)
        old_auth_token = auth_user_session_old.auth_token
        old_refresh_token = auth_user_session_old.refresh_token
        auth_user_session = UserAuthSession.create_session(self.first_user)
        self.assertEqual(
            UserAuthSession.objects.filter(user=self.first_user).count(), 1
        )
        self.assertNotEqual(old_auth_token, auth_user_session.auth_token)
        self.assertNotEqual(old_refresh_token, auth_user_session.refresh_token)

    def test_get_auth_user(self):
        auth_user_session = UserAuthSession.create_session(self.first_user)
        auth_token = auth_user_session.auth_token
        request = HttpRequest()
        request.headers = {UserAuthSession.AUTH_TOKEN_NAME: auth_token}
        auth_user = UserAuthSession.get_auth_user(request)

        self.assertEqual(auth_user, self.first_user)

    def test_throw_exception_no_auth_token(self):
        """test should throw a exception when trying to get a user based on request that doesn't
        have a auth token
        """
        UserAuthSession.create_session(self.first_user)
        request = HttpRequest()
        with self.assertRaises(Exception):
            UserAuthSession.get_auth_user(request)

    def test_should_throw_exception_when_invalid_token(self):
        request = HttpRequest()
        request.headers = {UserAuthSession.AUTH_TOKEN_NAME: "invalid token"}
        with self.assertRaises(Exception):
            UserAuthSession.get_auth_user(request)

    def test_is_authenticated(self):
        """test should raise PermissionDenied if the user isn't authenticated"""
        is_authenticated_permission = IsAuthenticated()
        with self.assertRaises(PermissionDenied):
            request = HttpRequest()
            request.user = None
            view = View()
            is_authenticated_permission.has_permission(request, view)

        with self.assertRaises(PermissionDenied):
            request = HttpRequest()
            User = namedtuple("User", "is_anonymous")
            user = User(True)
            request.user = user
            view = View()
            is_authenticated_permission.has_permission(request, view)

    def test_auth_middleware(self):
        auth_token = "auth-token"
        refresh_token = "refresh-token"
        expiration_datetime = datetime.now() + timedelta(days=20)
        UserAuthSession.objects.create(
            user=self.first_user,
            auth_token=auth_token,
            refresh_token=refresh_token,
            expiration_datetime=expiration_datetime,
        )
        get_response = Mock()
        request = HttpRequest()
        request.headers = {UserAuthSession.AUTH_TOKEN_NAME: auth_token}
        auth_middleware = AuthMiddleware(get_response)
        auth_middleware(request)
        new_request = get_response.call_args[0][0]
        self.assertEqual(new_request.user, self.first_user)

    def test_auth_middleware__invalid_token(self):
        auth_token = "auth-token"
        get_response = Mock()
        request = HttpRequest()
        request.headers = {UserAuthSession.AUTH_TOKEN_NAME: auth_token}
        auth_middleware = AuthMiddleware(get_response)
        response = auth_middleware(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_auth_middleware_expired_token(self):
        auth_token = "auth-token"
        refresh_token = "refresh-token"
        expiration_datetime = datetime.now() - timedelta(days=20)
        UserAuthSession.objects.create(
            user=self.first_user,
            auth_token=auth_token,
            refresh_token=refresh_token,
            expiration_datetime=expiration_datetime,
        )
        get_response = Mock()
        request = HttpRequest()
        request.headers = {UserAuthSession.AUTH_TOKEN_NAME: auth_token}
        auth_middleware = AuthMiddleware(get_response)
        response = auth_middleware(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
