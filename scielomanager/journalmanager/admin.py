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


admin.site.register(StudyArea)


class CollectionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(Collection, CollectionAdmin)


admin.site.register(Section)


class JournalAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)
    filter_horizontal = ('languages',)
    inlines = [JournalMissionInline]

admin.site.register(Journal, JournalAdmin)


class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(Institution, InstitutionAdmin)


class UserCollectionsInline(admin.TabularInline):
    model = UserCollections
    extra = 1
    can_delete = True


class UserProfileInline(admin.StackedInline):
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
    search_fields = ('publication_year', 'volume', 'number', 'journal__title')
    list_display = ('journal', 'volume', 'number', 'is_trashed', 'is_marked_up', '__unicode__',)

admin.site.register(Issue, IssueAdmin)


class SponsorAdmin(admin.ModelAdmin):
    filter_horizontal = ('collections',)

admin.site.register(Sponsor, SponsorAdmin)


class UseLicenseAdmin(admin.ModelAdmin):
    list_display = ('license_code', 'is_default', )

admin.site.register(UseLicense, UseLicenseAdmin)
admin.site.register(Language)
admin.site.register(TranslatedData)
admin.site.register(PressRelease)


# --------
# Article
# --------

def is_linked_to_issue(article):
    return bool(article.issue)
is_linked_to_issue.boolean = True


def is_linked_to_journal(article):
    return bool(article.journal)
is_linked_to_issue.boolean = True


class ArticleAdmin(admin.ModelAdmin):
    list_display = (
            'aid', 'xml_version', 'domain_key', 'updated_at',
            is_linked_to_issue, is_linked_to_journal,
    )
    list_filter = ('issue__journal',)
    date_hierarchy = 'updated_at'
    actions = ['link_to_issue', 'link_to_journal']
    readonly_fields = ('domain_key', 'xml', 'is_aop', 'xml_version', )

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

    def link_to_journal(self, request, queryset):
        for article in queryset:
            tasks.link_article_to_journal.delay(article.pk)

        count = queryset.count()
        if count >= 2:
            message = u'%s tasks were scheduled' % (count,)
        else:
            message = u'%s task was scheduled' % (count,)
        self.message_user(request, message)

    link_to_journal.short_description = u'Try to link with its journal'

admin.site.register(Article, ArticleAdmin)
