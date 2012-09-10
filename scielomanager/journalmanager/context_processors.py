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
        collections = models.get_user_collections(request.user.id)
        return {'user_collections': collections}
    else:
        return {}
