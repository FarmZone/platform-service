from django.contrib import admin
from .models import *


# class CartAdmin(admin.ModelAdmin):
#     model = Cart
#     fieldsets = (
#         (None, {'fields': ('user', 'seller_sub_product', 'price', 'discount')}),
#     )
#     list_display = ['user', 'seller_sub_product', 'price', 'discount']
#
#     def get_readonly_fields(self, request, obj=None):
#         if obj: # editing an existing object
#             return self.readonly_fields + ('user', 'seller_sub_product', 'price', 'discount')
#         return self.readonly_fields


class OrderDetailInlineAdmin(admin.TabularInline):
    model = OrderDetail
    fieldsets = (
        (None, {'fields': ('order', 'seller_sub_product', 'price', 'discount', 'qty', 'status')}),
    )
    list_display = ['order', 'seller_sub_product', 'price', 'discount', 'qty', 'status']
    extra = 0
    # readonly_fields = ('order', 'seller_sub_product', 'price', 'discount', 'qty', 'status',)
    verbose_name = "Order Detail"
    verbose_name_plural = "Order Details"
    # def get_readonly_fields(self, request, obj=None):
    #     if obj: # editing an existing object
    #         return self.readonly_fields + ('order', 'seller_sub_product', 'price', 'discount', 'qty', 'status')
    #     return self.readonly_fields


class OrderAdmin(admin.ModelAdmin):
    model = OrderDetail
    fieldsets = (
        (None, {'fields': ('user', 'total_price')}),
    )
    list_display = ['user', 'total_price']

    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields + ('user', 'total_price')
        return self.readonly_fields

    inlines = [
        OrderDetailInlineAdmin,
    ]


# admin.site.register(Cart, CartAdmin)
# admin.site.register(OrderDetail, OrderDetailAdmin)
admin.site.register(Orders, OrderAdmin)
