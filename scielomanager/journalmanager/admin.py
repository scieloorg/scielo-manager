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

class JournalHistoryInline(admin.StackedInline):
    model = JournalHist

class SectionTitleInline(admin.StackedInline):
    model = SectionTitle

class SectionAdmin(admin.ModelAdmin):
    inlines = [SectionTitleInline]

class JournalStudyAreaInline(admin.StackedInline):
    model = JournalStudyArea

class JournalAdmin(admin.ModelAdmin):
    list_display = ('title', 'validated')
    search_fields = ('title',)
    list_filter = ('is_available',)
    filter_horizontal = ('collections','languages')
    inlines = [JournalHistoryInline, JournalMissionInline,
        JournalStudyAreaInline]

class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('name','validated')
    search_fields = ('name',)

class UserProfileInline(admin.TabularInline):
    model = UserProfile

class UserCollectionsInline(admin.TabularInline):
    model = UserCollections
    extra = 1

class UserAdmin(admin.ModelAdmin):
    exclude = ('email', )
    inlines = (UserProfileInline, UserCollectionsInline)

class IssueAdmin(admin.ModelAdmin):
    list_display = ('journal', 'volume', 'number', 'is_available', 'is_marked_up')

class PublisherAdmin(admin.ModelAdmin):
    filter_horizontal = ('collections',)

admin.site.register(Journal, JournalAdmin)
admin.site.register(Institution, InstitutionAdmin)
admin.site.register(Collection, CollectionAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(UseLicense)
admin.site.register(Section, SectionAdmin)
admin.site.register(TranslatedData)
admin.site.register(Issue, IssueAdmin)
admin.site.register(Supplement)
admin.site.register(Publisher, PublisherAdmin)
admin.site.register(Language)
<<<<<<< HEAD

=======
>>>>>>> jamil/tk208
