from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from tools.models import ToolClassification, Tool, UserTool

# class ToolAdmin(admin.ModelAdmin):

admin.site.register(ToolClassification, MPTTModelAdmin)
admin.site.register(Tool)
admin.site.register(UserTool)
