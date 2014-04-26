from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from django_extensions.admin import ForeignKeyAutocompleteAdmin

from tools.models import ToolClassification, Tool, UserTool


class ToolAdmin(ForeignKeyAutocompleteAdmin):
    related_search_fields = {
        'parent': ('name', 'slug'),
        'classifications': ('name', 'slug'),
    }
    raw_id_fields = ('classifications', 'parent')


class UserToolAdmin(admin.ModelAdmin):
    raw_id_fields = ('tool_type', 'owner')


admin.site.register(ToolClassification, MPTTModelAdmin)
admin.site.register(Tool, ToolAdmin)
admin.site.register(UserTool, UserToolAdmin)
