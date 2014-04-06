from django.contrib import admin

from .models import (Hub, HubUser, HubOwner)


class OwnerInline(admin.StackedInline):
    model = HubOwner
    raw_id_fields = ('hub_user',)


class HubAdmin(admin.ModelAdmin):
    inlines = [OwnerInline]
    list_display = ['name', 'slug', 'is_enabled', 'is_private', 'user_count']
    prepopulated_fields = {"slug": ("name",)}


class HubUserAdmin(admin.ModelAdmin):
    list_display = ['user', 'hub', 'is_admin']
    raw_id_fields = ('user', 'hub')


class HubOwnerAdmin(admin.ModelAdmin):
    raw_id_fields = ('hub_user', 'hub')


admin.site.register(Hub, HubAdmin)
admin.site.register(HubUser, HubUserAdmin)
admin.site.register(HubOwner, HubOwnerAdmin)
