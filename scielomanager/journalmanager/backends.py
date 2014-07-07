#coding: utf-8
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend


class ModelBackend(ModelBackend):
    """
    Authenticate against the DJANGO login or user e-mail

    Use the login name, and password or userprofile.email and password
    """

    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(Q(username=username)| Q(email=username), is_active=True)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
