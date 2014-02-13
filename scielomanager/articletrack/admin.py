# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import *

class CheckinAdmin(admin.ModelAdmin):
	list_display = ('package_name', 'attempt_ref', 'uploaded_at', 'created_at')
	search_fields = ('package_name',)
	readonly_fields = ('created_at',)

admin.site.register(Checkin, CheckinAdmin)


class CommentInline(admin.StackedInline):
    model = Comment

class TicketAdmin(admin.ModelAdmin):
	list_display = ('article', 'title', 'author', 'is_open', 'started_at', 'finished_at')
	readonly_fields = ('started_at', 'is_open')
	inlines = [CommentInline, ]

admin.site.register(Ticket, TicketAdmin)

class ArticleAdmin(admin.ModelAdmin):
	list_display = ('article_title', 'articlepkg_ref', 'journal_title')

admin.site.register(Article, ArticleAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('date', 'ticket', 'author')

admin.site.register(Comment, CommentAdmin)
admin.site.register(Notice)
