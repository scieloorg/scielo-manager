# -*- coding: utf-8 -*-
from django.contrib import admin
from . import models


class TeamAdmin(admin.ModelAdmin):

    def display_member(self, obj):
        list_members = []
        if obj.member:
            for pr in obj.member.all():
                list_members.append(pr.username)
        return ' | '.join(list_members)

    display_member.short_description = 'Members'

    list_display = ('name', 'display_member')
    filter_horizontal = ("member",)
    search_fields = ('name',)

admin.site.register(models.Team, TeamAdmin)


class CheckinAdmin(admin.ModelAdmin):
    list_display = ('package_name', 'attempt_ref', 'uploaded_at', 'created_at')
    search_fields = ('package_name',)
    readonly_fields = ('created_at',)

admin.site.register(models.Checkin, CheckinAdmin)


class CommentInline(admin.StackedInline):
    model = models.Comment


class TicketAdmin(admin.ModelAdmin):
    list_display = ('article', 'title', 'author', 'is_open', 'started_at', 'finished_at')
    readonly_fields = ('started_at', 'is_open')
    inlines = [CommentInline, ]

admin.site.register(models.Ticket, TicketAdmin)


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('article_title', 'articlepkg_ref', 'journal_title')

admin.site.register(models.Article, ArticleAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'updated_at', 'ticket', 'author')
    readonly_fields = ('created_at', 'updated_at',)

admin.site.register(models.Comment, CommentAdmin)


class CheckinWorkflowLogAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'checkin', 'user', 'status', 'description')
    readonly_fields = ('created_at', 'checkin', 'user', 'status', 'description')

admin.site.register(models.CheckinWorkflowLog, CheckinWorkflowLogAdmin)


class NoticeAdmin(admin.ModelAdmin):
    search_fields = ('message',)
    list_filter = ('status', 'checkpoint')
    list_display = ('checkin', 'stage', 'checkpoint', 'message', 'status')

admin.site.register(models.Notice, NoticeAdmin)
