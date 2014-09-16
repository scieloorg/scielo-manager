# -*- coding: utf-8 -*-
from django.contrib import admin
from . import models


class EditorialMemberInline(admin.StackedInline):
    model = models.EditorialMember


class EditorialBoardAdmin(admin.ModelAdmin):
    inlines = [EditorialMemberInline, ]

admin.site.register(models.EditorialBoard, EditorialBoardAdmin)

class RoleTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'weight', )
    search_fields = ('name', 'weight', )

admin.site.register(models.RoleType, RoleTypeAdmin)
