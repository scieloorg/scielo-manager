# -*- coding: utf-8 -*-
from django.contrib import admin
from . import models


class EditorialMemberInline(admin.StackedInline):
    model = models.EditorialMember
    fieldsets = (
        (None,
            {'fields':('role', 'first_name', 'last_name', 'order')}
        ),
        ('Optional fields',
            {
                'fields':  ('email', 'institution', 'link_cv', 'city', 'state', 'country', 'research_id', 'orcid'),
                'classes':('collapse',),
            }
        ),
    )


class EditorialBoardAdmin(admin.ModelAdmin):
    inlines = [EditorialMemberInline, ]

    def journal(self, obj):
        return obj.issue.journal

    def issue_publication_year(self, obj):
        return obj.issue.publication_year

    search_fields = ('issue__journal__title', 'issue__volume', 'issue__publication_year')
    list_display = ('__unicode__', 'issue_publication_year', 'issue', 'journal')


class RoleTypeTranslationInline(admin.TabularInline):
    model = models.RoleTypeTranslation


class RoleTypeAdmin(admin.ModelAdmin):
    model = models.RoleType
    list_display = ('name', )
    search_fields = ('name', )
    inlines = [RoleTypeTranslationInline, ]


admin.site.register(models.EditorialBoard, EditorialBoardAdmin)
admin.site.register(models.RoleType, RoleTypeAdmin)
