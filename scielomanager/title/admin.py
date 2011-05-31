# -*- coding: utf-8 -*-

from django.contrib import admin
from scielomanager.title.models import *

class TitleAdmin(admin.ModelAdmin):
    list_display = ('title', 'validated')
    search_fields = ('title',)

class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name','sponsor','validated')    
    search_fields = ('name','sponsor')
    
if Title not in admin.site._registry:
    admin.site.register(Title, TitleAdmin)

if Publisher not in admin.site._registry:
    admin.site.register(Publisher, PublisherAdmin)
