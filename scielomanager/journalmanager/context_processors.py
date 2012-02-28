# coding: utf-8
from django.conf import settings

def from_settings(request):
    """
    Provides certain settings in the templates.

    Searches for an associative list named AVAILABLE_IN_TEMPLATES
    in settings.py.
    """
    try:
        return dict(settings.AVAILABLE_IN_TEMPLATES)
    except (ValueError, AttributeError):
        return {}