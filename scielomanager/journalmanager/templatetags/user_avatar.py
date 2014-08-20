# -*- coding: utf-8 -*-

# Usage:
#
# {% user_avatar_url user [size_in_px|"small"|"medium"|"large"] %}
#
# user:
# django.contrib.auth.models.User object
#
# size_in_px:
# size of the result avatar (size_in_px x size_in_px)
#
# Examples:
# {% user_avatar_url request.user "18" %}
# {% user_avatar_url request.user "small" %}
# {% user_avatar_url request.user "medium" %}
# {% user_avatar_url request.user "large" %}

import urllib
from django import template
from django.conf import settings
from journalmanager.models import UserProfile

SIZE_LARGE = 64
SIZE_MEDIUM = 32
SIZE_SMALL = 18

register = template.Library()
def user_avatar_url(user, size):
    size = size.lower()
    if size == 'large':
        size = SIZE_LARGE
    elif size == 'medium':
        size = SIZE_MEDIUM
    elif size == 'small':
        size = SIZE_SMALL
    elif size.isdigit() and int(size) > 0:
        size = int(size)
    else:
        return '' # unknow size, no photo
    try:
        user_gravatar_id = user.email
    except AttributeError: # possible user is None
        return ''
    else:
        if user_gravatar_id:
            params = urllib.urlencode({'s': size, 'd': 'mm'})
            gravatar_url = getattr(settings, 'GRAVATAR_BASE_URL', 'https://secure.gravatar.com')
            avartar_url = '{0}/avatar/{1}?{2}'.format(gravatar_url, user_gravatar_id, params)
            return avartar_url
        else:
            return ''

register.simple_tag(user_avatar_url)
