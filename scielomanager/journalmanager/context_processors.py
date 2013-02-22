# coding: utf-8
from django.conf import settings
from journalmanager import models
from maintenancewindow import models as maintenance_models


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


def show_system_notes(request):
    """
    Add system notes as maintenance events, notes, etc to the context
    """
    def wrap():
        return maintenance_models.Event.objects.scheduled_events()

    return {'system_notes': wrap}


def show_system_notes_blocking_users(request):
    """
    Add system notes that are blockin the user access
    as maintenance events, notes, etc to the context
    """
    def wrap():
        return maintenance_models.Event.objects.blocking_users_scheduled_event()

    return {'blocking_users_system_note': wrap}


def on_maintenance(request):
    """
    Add on_maintenance item to the context. Defining if there is or not active
    maintenance events.
    """
    def wrap():
        return maintenance_models.Event.on_maintenance()

    return {'on_maintenance': wrap}


def show_user_collections(request):
    """
    Adds `user_collections` item to the context, which is a
    queryset of collections the user relates to.
    """
    def wrap():
        return models.Collection.objects.all_by_user(request.user)

    if request.user.is_authenticated():
        return {'user_collections': wrap}
    else:
        return {}


def add_default_collection(request):
    if request.user.is_authenticated():
        try:
            collection = models.Collection.objects.get_default_by_user(request.user)
        except models.Collection.DoesNotExist:
            return {}
        else:

            def wrap_is_managed_by_user():
                return collection.is_managed_by_user(request.user)

            return {
                'default_collection': collection,
                'is_manager_of_default_collection': wrap_is_managed_by_user
                }
    else:
        return {}
