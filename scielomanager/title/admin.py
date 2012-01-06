# -*- coding: utf-8 -*-
from django.contrib import admin
from scielomanager.title.models import *
from django.contrib.auth.admin import UserAdmin

admin.site.unregister(User)

class CollectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'validated')
    search_fields = ('name',)
    
class TitleMissionInline(admin.StackedInline):
    model = TitleMission
    
class TitleOtherFormsInline(admin.StackedInline):
    model = TitleOtherForms

class ShortTitleOtherFormsInline(admin.StackedInline):
    model = ShortTitleOtherForms

class TitleAdmin(admin.ModelAdmin):
    list_display = ('title', 'validated')
    search_fields = ('title',)
    inlines = [TitleMissionInline,TitleOtherFormsInline,ShortTitleOtherFormsInline]
   
class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name','sponsor','validated')    
    search_fields = ('name','sponsor')
    
class UserProfileInline(admin.StackedInline):
    model = UserProfile

class UserProfileAdmin(UserAdmin):
    list_display = ('username', 'email',  )
    search_fields = ['username','email', 'collection']
    inlines = [UserProfileInline]
    
if Title not in admin.site._registry:
    admin.site.register(Title, TitleAdmin)

if Publisher not in admin.site._registry:
    admin.site.register(Publisher, PublisherAdmin)

if Collection not in admin.site._registry:
    admin.site.register(Collection, CollectionAdmin)

admin.site.register(User, UserProfileAdmin)