from django.contrib import admin
from .models import *


class SupportAdmin(admin.ModelAdmin):
    model = Support
    fieldsets = (
        (None, {'fields': ('support_category', 'seller', 'user', 'status', 'comment')}),
    )
    list_display = ['support_category', 'seller', 'user', 'status', 'comment']
    search_fields = ['name']


class SupportCategoryAdmin(admin.ModelAdmin):
    model = SupportCategory
    fieldsets = (
        (None, {'fields': ('category_code', 'name', 'description')}),
    )
    readonly_fields = ('category_code',)
    list_display = ['category_code', 'name', 'description']
    search_fields = ['name']


admin.site.register(Support, SupportAdmin)
admin.site.register(SupportCategory, SupportCategoryAdmin)
