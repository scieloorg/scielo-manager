# -*- encoding: utf-8 -*-

# Because Django deletes related objects by default,
# deleting the ContentType objects will also remove the
# related django.contrib.auth.models.Permission objects
# (and the many-to-many associations with users and groups).

from django.contrib.contenttypes.models import ContentType
ContentType.objects.filter(app_label='articletrack').delete()
