# -*- coding: utf-8 -*-
from django.contrib import admin
from scielomanager.journalmanager.models import *
from django.contrib.auth.admin import UserAdmin

admin.site.unregister(User)

class CollectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'validated')
    search_fields = ('name',)

class JournalMissionInline(admin.StackedInline):
    model = JournalMission

class JournalTextLanguageInline(admin.StackedInline):
    model = JournalTextLanguage

class JournalHistoryInline(admin.StackedInline):
    model = JournalHist

class JournalSectionsInline(admin.StackedInline):
    model = Section

class JournalAdmin(admin.ModelAdmin):
    list_display = ('title', 'validated')
    search_fields = ('title',)
    list_filter = ('is_available',)
    inlines = [JournalHistoryInline, JournalTextLanguageInline, JournalMissionInline, JournalSectionsInline]

class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('name','validated')
    search_fields = ('name',)

#class UserProfileInline(admin.StackedInline):
    #model = UserProfile

#class UserProfileAdmin(UserAdmin):
    #inlines = [UserProfileInline,UserCollectionsInline]

class UserCollectionsInline(admin.TabularInline):
    model = UserCollections
    extra = 1

class UserAdmin(admin.ModelAdmin):
    inlines = (UserCollectionsInline,)

class IssueAdmin(admin.ModelAdmin):
    list_display = ('journal', 'volume', 'number', 'is_available', 'is_marked_up')

if Journal not in admin.site._registry:
    admin.site.register(Journal, JournalAdmin)

if Institution not in admin.site._registry:
    admin.site.register(Institution, InstitutionAdmin)

if Collection not in admin.site._registry:
    admin.site.register(Collection, CollectionAdmin)

admin.site.register(User, UserAdmin)
admin.site.register(UseLicense)
admin.site.register(Section)
admin.site.register(TranslatedData)
admin.site.register(Issue, IssueAdmin)
admin.site.register(Supplement)

if IndexingCoverage not in admin.site._registry:
    admin.site.register(IndexingCoverage)
