# -*- coding: utf-8 -*-
from django.contrib import admin
from scielomanager.journalmanager.models import *
from django.contrib.auth.admin import UserAdmin

class JournalMissionInline(admin.StackedInline):
    model = JournalMission

class SectionTitleInline(admin.StackedInline):
    model = SectionTitle

class JournalStudyAreaInline(admin.StackedInline):
    model = JournalStudyArea

class CollectionAdmin(admin.ModelAdmin):

    def queryset(self, request):
        return Collection.nocacheobjects

    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(Collection, CollectionAdmin)

class SectionAdmin(admin.ModelAdmin):

    def queryset(self, request):
        return Section.nocacheobjects

admin.site.register(Section, SectionAdmin)

class JournalAdmin(admin.ModelAdmin):

    def queryset(self, request):
        return Journal.nocacheobjects

    list_display = ('title',)
    search_fields = ('title',)
    filter_horizontal = ('collections','languages')
    inlines = [JournalMissionInline,
        JournalStudyAreaInline]

admin.site.register(Journal, JournalAdmin)

class InstitutionAdmin(admin.ModelAdmin):

    def queryset(self, request):
        return Institution.nocacheobjects

    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(Institution, InstitutionAdmin)

class UserCollectionsInline(admin.TabularInline):

    def queryset(self, request):
        return UserCollections.nocacheobjects

    model = UserCollections
    extra = 1
    can_delete = True

class UserProfileInline(admin.StackedInline):

    def queryset(self, request):
        return UserProfile.nocacheobjects

    model = UserProfile
    max_num = 1
    can_delete = True

class UserAdmin(UserAdmin):
    inlines = (UserProfileInline, UserCollectionsInline)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

class IssueAdmin(admin.ModelAdmin):

    def queryset(self, request):
        return Issue.nocacheobjects

    list_display = ('journal', 'volume', 'number', 'is_trashed', 'is_marked_up')

admin.site.register(Issue, IssueAdmin)

class SponsorAdmin(admin.ModelAdmin):

    def queryset(self, request):
        return Sponsor.nocacheobjects

    filter_horizontal = ('collections',)

admin.site.register(Sponsor, SponsorAdmin)

class PublisherAdmin(admin.ModelAdmin):

    def queryset(self, request):
        return Publisher.nocacheobjects

    filter_horizontal = ('collections',)

admin.site.register(Publisher, PublisherAdmin)

class UseLicenseAdmin(admin.ModelAdmin):

    def queryset(self, request):
        return UseLicense.nocacheobjects

admin.site.register(UseLicense, UseLicenseAdmin)

class LanguageAdmin(admin.ModelAdmin):

    def queryset(self, request):
        return Language.nocacheobjects

admin.site.register(Language, LanguageAdmin)

class TranslatedDataAdmin(admin.ModelAdmin):

    def queryset(self, request):
        return TranslatedData.nocacheobjects

admin.site.register(TranslatedData)

class SupplementAdmin(admin.ModelAdmin):

    def queryset(self, request):
        return Supplement.nocacheobjects

admin.site.register(Supplement, SupplementAdmin)

class JournalPublicationEventsAdmin(admin.ModelAdmin):

    def queryset(self, request):
        return JournalPublicationEvents.nocacheobjects

    list_display = ['journal', 'status', 'created_at',]
    list_filter = ['status',]
    search_fields = ['journal',]

admin.site.register(JournalPublicationEvents, JournalPublicationEventsAdmin)


