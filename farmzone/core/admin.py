from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from ajax_select import make_ajax_form


class UserAdmin(BaseUserAdmin):
    model = User
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email', 'full_name', 'first_name', 'last_name', 'date_joined', 'img_orig', 'img_thumb',)}),
        ('Permissions', {'fields': ('is_admin', 'is_staff', 'is_superuser', 'groups', 'is_active')}),
    )
    list_display = ['username', 'first_name', 'last_name', 'is_active', 'full_name']
    search_fields = ['full_name']


class UserRolesAdmin(admin.ModelAdmin):
    model = UserRoles

    search_fields = ['name', 'alias_name']


class PhoneNumberAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number', 'is_active', 'type']
    search_fields = ['user__full_name', 'phone_number']

    form = make_ajax_form(PhoneNumber, {
            # fieldname: channel_name
            'user': 'users'
    })


class AppConfigurationAdmin(admin.ModelAdmin):
    list_display = ['key', 'value']
    search_fields = ['key']


class StateCodeAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'is_active']
    search_fields = ['name']


class AddressAdmin(admin.ModelAdmin):
    list_display = ['address_line1', 'address_line2', 'address_line3', 'state']
    search_fields = ['address_line1']


admin.site.register(User, UserAdmin)
admin.site.register(UserRoles, UserRolesAdmin)
admin.site.register(PhoneNumber, PhoneNumberAdmin)
admin.site.register(AppConfiguration, AppConfigurationAdmin)
admin.site.unregister(Group)
admin.site.register(StateCode, StateCodeAdmin)
admin.site.register(Address, AddressAdmin)
