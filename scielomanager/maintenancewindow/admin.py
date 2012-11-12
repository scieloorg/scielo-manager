from django.contrib import admin
from scielomanager.maintenancewindow.models import *


class EventAdmin(admin.ModelAdmin):

    list_display = ('title', 'begin_at', 'end_at')

admin.site.register(Event, EventAdmin)
