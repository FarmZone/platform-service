from django.contrib import admin

from .models import *


class SellerAdmin(admin.ModelAdmin):
    model = Seller
    fieldsets = (
        (None, {'fields': ('name', 'is_active')}),
    )
    list_display = ['seller_code', 'name', 'is_active']
    search_fields = ['name']


class SellerOwnerAdmin(admin.ModelAdmin):
    model = SellerOwner
    list_display = ['seller', 'user', 'is_active']


class PreferredSellerAdmin(admin.ModelAdmin):
    model = PreferredSeller
    list_display = ['user', 'seller', 'is_primary']


class SellerSubProductAdmin(admin.ModelAdmin):
    model = SellerSubProduct
    list_display = ['seller', 'sub_product', 'price', 'discount', 'is_active']

    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields + ('seller', 'sub_product', 'price', 'discount', 'is_active')
        return self.readonly_fields


class UserProductAdmin(admin.ModelAdmin):
    model = UserProduct
    list_display = ['user', 'seller', 'product_name', 'product_serial_no']


class SellerDeviceAdmin(admin.ModelAdmin):
    list_display = ['user', 'fcm_device']
    search_fields = ['user__full_name']


admin.site.register(Seller, SellerAdmin)
admin.site.register(SellerOwner, SellerOwnerAdmin)
admin.site.register(PreferredSeller, PreferredSellerAdmin)
admin.site.register(SellerSubProduct, SellerSubProductAdmin)
admin.site.register(UserProduct, UserProductAdmin)
admin.site.register(SellerDevice, SellerDeviceAdmin)
