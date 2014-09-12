from django.contrib import admin
from audit_log.models import AuditLogEntry, AuditLogEntryPermission


class AuditLogEntryAdmin(admin.ModelAdmin):
    list_display = ['action_time', 'user', 'action_flag', 'object_repr', \
                    'content_type', 'object_id', 'change_message']
    readonly_fields = ['action_time', 'user', 'action_flag', 'object_repr', \
                       'content_type', 'object_id', 'change_message', \
                       'old_values', 'new_values']
    list_filter = ('content_type', 'action_time')


class AuditLogEntryPermissionAdmin(admin.ModelAdmin):
    list_display = ['user', 'content_type']
    list_filter = ('user', 'content_type')

admin.site.register(AuditLogEntry, AuditLogEntryAdmin)
admin.site.register(AuditLogEntryPermission, AuditLogEntryPermissionAdmin)
