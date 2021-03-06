from django.contrib import admin
from .models import *


class SupportAdmin(admin.ModelAdmin):
    model = Support
    fieldsets = (
        (None, {'fields': ('support_category', 'order_detail', 'user', 'status', 'comment')}),
    )
    list_display = ['support_category', 'order_detail', 'user', 'status', 'comment']
    search_fields = ['name']


class SupportCategoryAdmin(admin.ModelAdmin):
    model = SupportCategory
    fieldsets = (
        (None, {'fields': ('category_code', 'name', 'type', 'description')}),
    )
    readonly_fields = ('category_code',)
    list_display = ['category_code', 'name', 'type', 'description']
    search_fields = ['name']


admin.site.register(Support, SupportAdmin)
admin.site.register(SupportCategory, SupportCategoryAdmin)
