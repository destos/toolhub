from django.contrib import admin

from .models import Transaction, LendingAction


class TransactionAdmin(admin.ModelAdmin):
    raw_id_fields = ('hub', 'tool', 'lendee')


class LendingActionAdmin(admin.ModelAdmin):
    raw_id_fields = ('transaction',)


admin.site.register(Transaction, TransactionAdmin)
admin.site.register(LendingAction, LendingActionAdmin)
