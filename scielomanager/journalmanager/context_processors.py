# coding: utf-8
from django.conf import settings

from journalmanager import models


def dynamic_template_inheritance(request):
    """
    Changes between base_lv0.html e base_lv1.html
    """
    if request.GET.get('popup', None):
        return {'dynamic_tpl': 'base_lv0.html'}
    else:
        return {'dynamic_tpl': 'base_lv1.html'}


def access_to_settings(request):
    return {'SETTINGS': settings}


def show_user_collections(request):
    """
    Adds `user_collections` item to the context, which is a
    queryset of collections the user relates to.
    """
    if request.user.is_authenticated():
        collections = models.Collection.objects.all_by_user(request.user)
        return {'user_collections': collections}
    else:
        return {}


def add_default_collection(request):
    if request.user.is_authenticated():
        try:
            collection = models.Collection.objects.get_default_by_user(request.user)
            return {
                'default_collection': collection,
                'is_manager_of_default_collection': collection.is_managed_by_user(request.user)
                }
        except models.Collection.DoesNotExist:
            return {}
    else:
        return {}
