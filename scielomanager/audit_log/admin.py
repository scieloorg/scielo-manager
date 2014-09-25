from django.contrib import admin
from audit_log.models import AuditLogEntry, AuditLogEntryPermission



class AuditLogEntryAdmin(admin.ModelAdmin):

    def get_action_flag(self, obj):
        if obj.action_flag == 1: # additon
            return "<span style='color: green;'>ADDED</span>"
        elif obj.action_flag == 2: # change
            return "<span style='color: orange;'>CHANGED</span>"
        else:
            return "<span style='color: red;'>DELETED</span>"
    get_action_flag.short_description = 'Action'
    get_action_flag.allow_tags = True
    get_action_flag.admin_order_field = 'action_flag'


    list_display = ['action_time', 'user', 'get_action_flag', 'object_repr', \
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
