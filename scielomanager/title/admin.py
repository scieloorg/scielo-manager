# -*- coding: utf-8 -*-

from django.contrib import admin
from scielomanager.title.models import *

class TitleAdmin(admin.ModelAdmin):
    list_display = ('title',)
    
    
if Title not in admin.site._registry:
    admin.site.register(Title, TitleAdmin)
