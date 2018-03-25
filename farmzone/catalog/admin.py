from django.contrib import admin
from .models import *


class SubProductInlineAdmin(admin.TabularInline):
    model = SubProduct
    fieldsets = (
        (None, {'fields': ('sub_product_code', 'name', 'display_name', 'description', 'img_orig', 'img_thumb')}),
    )
    readonly_fields = ('sub_product_code',)
    extra = 0
    verbose_name = "Sub Product"
    verbose_name_plural = "Sub products"


class ProductDetailInlineAdmin(admin.TabularInline):
    model = ProductDetail
    fieldsets = (
        (None, {'fields': ('key', 'value')}),
    )
    extra = 0
    verbose_name = "Product Detail"
    verbose_name_plural = "Product Details"


class ProductAdmin(admin.ModelAdmin):
    model = Product
    fieldsets = (
        (None, {'fields': ('product_code', 'name', 'product_category', 'display_name', 'description')}),
    )
    list_display = ['product_code', 'product_category', 'name', 'display_name', 'description']
    readonly_fields = ('product_code',)
    search_fields = ['name']
    inlines = [
        SubProductInlineAdmin,
        ProductDetailInlineAdmin
    ]


class ProductInlineAdmin(admin.TabularInline):
    model = Product
    fieldsets = (
        (None, {'fields': ('product_code', 'name', 'product_category', 'display_name', 'description', 'img_orig', 'img_thumb')}),
    )
    list_display = ['product_code', 'product_category', 'name', 'display_name', 'description']
    readonly_fields = ('product_code',)
    search_fields = ['name']
    extra = 0
    inlines = [
        SubProductInlineAdmin,
        ProductDetailInlineAdmin
    ]


class ProductCategoryAdmin(admin.ModelAdmin):
    model = ProductCategory
    fieldsets = (
        (None, {'fields': ('category_code', 'name', 'display_name', 'description')}),
    )
    readonly_fields = ('category_code',)
    list_display = ['category_code', 'name', 'display_name', 'description']
    search_fields = ['name']
    inlines = [
        ProductInlineAdmin,
    ]


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductCategory, ProductCategoryAdmin)
