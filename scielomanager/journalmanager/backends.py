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

    def get_group_permissions(self, user_obj):
        """
        Returns a set of permission strings that this user has through his/her
        groups.
        """
        if not hasattr(user_obj, '_group_perm_cache'):
            if user_obj.is_superuser:
                perms = Permission.objects.all()
            else:
                perms = Permission.objects.filter(group__user=user_obj)
            perms = perms.values_list('content_type__app_label', 'codename').order_by()
            user_obj._group_perm_cache = set(["%s.%s" % (ct, name) for ct, name in perms])
        return user_obj._group_perm_cache

    def get_all_permissions(self, user_obj):
        if user_obj.is_anonymous():
            return set()
        if not hasattr(user_obj, '_perm_cache'):
            user_obj._perm_cache = set([u"%s.%s" % (p.content_type.app_label, p.codename) for p in user_obj.user_permissions.select_related()])
            user_obj._perm_cache.update(self.get_group_permissions(user_obj))
        return user_obj._perm_cache

    def has_perm(self, user_obj, perm):
        if not user_obj.is_active:
            return False
        return perm in self.get_all_permissions(user_obj)

    def has_module_perms(self, user_obj, app_label):
        """
        Returns True if user_obj has any permissions in the given app_label.
        """
        if not user_obj.is_active:
            return False
        for perm in self.get_all_permissions(user_obj):
            if perm[:perm.index('.')] == app_label:
                return True
        return False

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None