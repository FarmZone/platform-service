from django.contrib import admin
from .models import *


class BuyerDeviceAdmin(admin.ModelAdmin):
    list_display = ['user', 'fcm_device']
    search_fields = ['user__full_name']


admin.site.register(BuyerDevice, BuyerDeviceAdmin)