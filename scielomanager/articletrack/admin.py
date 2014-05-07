# -*- coding: utf-8 -*-
from django.contrib import admin
from . import models


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


class CheckinWorflowLogAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'checkin', 'user', 'status', 'description')
    readonly_fields = ('created_at', 'checkin', 'user', 'status', 'description')


admin.site.register(models.CheckinWorflowLog, CheckinWorflowLogAdmin)

admin.site.register(models.Notice)