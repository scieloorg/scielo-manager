from django.contrib import admin
from scielomanager.maintenancewindow.models import *


class EventAdmin(admin.ModelAdmin):

    list_display = ('title', 'begin_at', 'end_at', 'is_blocking_users', 'is_finished')

admin.site.register(Event, EventAdmin)
