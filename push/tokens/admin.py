from django.contrib import admin
from tokens.models import Token


class TokenAdmin(admin.ModelAdmin):
    # by default auto_now_add fields are not displayed. We want to display (but not edit) token creation date
    list_display = ('token', 'owner', 'date_created',)
    ordering = ('-date_created',)
    readonly_fields = ('date_created', 'token', 'name',)
    search_fields = ['token', 'owner__username']
    raw_id_fields = ['owner', 'apns_device', 'gcm_device', ]


admin.site.register(Token, TokenAdmin)
