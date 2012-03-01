# -*- encoding: utf-8 -*-
from django.contrib.auth import authenticate
from django.contrib.auth.models import User, get_hexdigest
from django.core.exceptions import ObjectDoesNotExist

class ModelBackend(object):
    """
    Authenticate against the DJANGO login or user e-mail

    Use the login name, and password or user.email and password
    """

    def authenticate(self, username=None, password=None):
        # Autenticando com metodo de autenticacao padrao do Django.

        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            # Autenticando contra email do usuário
            try:
                user = User.objects.get(email=username)
                if user.check_password(password):
                    return user
            except User.DoesNotExist:
                return None #User nao existe
        
        return None


    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None