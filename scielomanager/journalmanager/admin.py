# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin.templatetags.admin_static import static
from tastypie.models import ApiAccess

from .models import *
from .forms import UserChangeForm, UserCreationForm
from . import tasks


admin.site.register(ApiAccess)


class JournalMissionInline(admin.StackedInline):
    model = JournalMission


class SectionTitleInline(admin.StackedInline):
    model = SectionTitle


class StudyAreaAdmin(admin.ModelAdmin):

    def queryset(self, request):
        return StudyArea.nocacheobjects

admin.site.register(StudyArea, StudyAreaAdmin)


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
    filter_horizontal = ('languages',)
    inlines = [JournalMissionInline]

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
    def profile_email_notifications(self, user):
        """
        display a green/red icon if user accepts or not email notifications.
        if for some reason, the user don't have a UserProfile, it returns a (?) icon.
        """
        if user.get_profile():
            email_notifications = user.get_profile().email_notifications
            icon_url = static('admin/img/icon-%s.gif' % {True: 'yes', False: 'no', None: 'unknown'}[email_notifications])
            return '<img src="{0}" alt="{1}" />'.format(icon_url, email_notifications)
        else:
            icon_url = static('admin/img/icon-icon-unknown.gif')
            return '<img src="{0}" alt="NO PROFILE" />no profile!' % icon_url
    profile_email_notifications.short_description = 'Email Notifications'
    profile_email_notifications.allow_tags = True

    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'profile_email_notifications', )
    inlines = (UserProfileInline, UserCollectionsInline)
    form = UserChangeForm
    add_form = UserCreationForm
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('username', 'password1', 'password2', 'email')
            }
        ),
    )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class IssueAdmin(admin.ModelAdmin):

    def queryset(self, request):
        return Issue.nocacheobjects

    search_fields = ('publication_year', 'volume', 'number', 'journal__title')
    list_display = ('journal', 'volume', 'number', 'is_trashed', 'is_marked_up', '__unicode__',)

admin.site.register(Issue, IssueAdmin)


class SponsorAdmin(admin.ModelAdmin):

    def queryset(self, request):
        return Sponsor.nocacheobjects

    filter_horizontal = ('collections',)

admin.site.register(Sponsor, SponsorAdmin)


class UseLicenseAdmin(admin.ModelAdmin):
    list_display = ('license_code', 'is_default', )
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


class PressReleaseAdmin(admin.ModelAdmin):

    def queryset(self, request):
        return PressRelease.nocacheobjects

admin.site.register(PressRelease, PressReleaseAdmin)


#--------
# Article
#--------
def is_linked_to_the_issue(article):
    return bool(article.issue)
is_linked_to_the_issue.boolean = True


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('xml_doi', 'aid', 'abbrev_journal_title', 'issue',
                    'updated_at', is_linked_to_the_issue)
    list_filter = ('issue__journal',)
    date_hierarchy = 'updated_at'
    actions = ['link_to_issue',]
    readonly_fields = ('article_id_slug', 'xml', 'is_generated',)

    def queryset(self, request):
        return Article.nocacheobjects

    def link_to_issue(self, request, queryset):
        for article in queryset:
            tasks.link_article_to_issue.delay(article.pk)

        count = queryset.count()
        if count >= 2:
            message = u'%s tasks were scheduled' % (count,)
        else:
            message = u'%s task was scheduled' % (count,)
        self.message_user(request, message)

    link_to_issue.short_description = u'Try to link with its issue'

admin.site.register(Article, ArticleAdmin)
