# -*- coding: utf-8 -*-
from django.contrib import admin
from scielomanager.journalmanager.models import *
from django.contrib.auth.admin import UserAdmin
from django.core.cache import cache 

admin.site.unregister(User)

class CustomModelAdmin(admin.ModelAdmin):

    def queryset(self, request):
        cache.clear()
        qs = super(admin.ModelAdmin, self).queryset(request)
        return qs 

class CollectionAdmin(CustomModelAdmin):
    list_display = ('name', 'validated')
    search_fields = ('name',)

admin.site.register(Collection, CollectionAdmin)

class JournalMissionInline(admin.StackedInline):
    model = JournalMission

class JournalHistoryInline(admin.StackedInline):
    model = JournalHist

class SectionTitleInline(admin.StackedInline):
    model = SectionTitle

class SectionAdmin(CustomModelAdmin):
    inlines = [SectionTitleInline]

admin.site.register(Section, SectionAdmin)

class JournalStudyAreaInline(admin.StackedInline):
    model = JournalStudyArea

class JournalAdmin(CustomModelAdmin):
    list_display = ('title', 'validated')
    search_fields = ('title',)
    list_filter = ('is_available',)
    filter_horizontal = ('collections','languages')
    inlines = [JournalHistoryInline, JournalMissionInline,
        JournalStudyAreaInline]

admin.site.register(Journal, JournalAdmin)

class InstitutionAdmin(CustomModelAdmin):
    list_display = ('name','validated')
    search_fields = ('name',)

admin.site.register(Institution, InstitutionAdmin)

class UserProfileInline(admin.TabularInline):
    model = UserProfile

class UserCollectionsInline(admin.TabularInline):
    model = UserCollections
    extra = 1

class UserAdmin(CustomModelAdmin):
    exclude = ('email', )
    inlines = (UserProfileInline, UserCollectionsInline)

admin.site.register(User, UserAdmin)

class IssueAdmin(CustomModelAdmin):
    list_display = ('journal', 'volume', 'number', 'is_available', 'is_marked_up')

admin.site.register(Issue, IssueAdmin)

class PublisherAdmin(CustomModelAdmin):
    filter_horizontal = ('collections',)

admin.site.register(Publisher, PublisherAdmin)

class UseLicenseAdmin(CustomModelAdmin):
    pass

admin.site.register(UseLicense, UseLicenseAdmin)

class LanguageAdmin(CustomModelAdmin):
    pass

admin.site.register(Language, LanguageAdmin)

class TranslatedDataAdmin(CustomModelAdmin):
    pass

admin.site.register(TranslatedData)

class SupplementAdmin(CustomModelAdmin):
    pass

admin.site.register(Supplement, SupplementAdmin)
