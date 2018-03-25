from rest_framework.authtoken.admin import TokenAdmin
from rest_framework.authtoken.models import Token
from ajax_select import make_ajax_form
from django.contrib import admin


class CustomTokenAdmin(TokenAdmin):
    form = make_ajax_form(Token, {
        # fieldname: channel_name
        'user': 'users'
    })
    search_fields = ["user__full_name"]


admin.site.unregister(Token)
admin.site.register(Token, CustomTokenAdmin)


