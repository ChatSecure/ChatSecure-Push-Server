from django.contrib import admin
from tokens.models import Token


class TokenAdmin(admin.ModelAdmin):
    # by default auto_now_add fields are not displayed. We want to display (but not edit) token creation date
    readonly_fields = ('date_created',)

admin.site.register(Token, TokenAdmin)
