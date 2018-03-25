import logging
from django.db import models
from farmzone.core.models import TimestampedModel
from django.db.models.signals import post_save
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage
from farmzone import util_config as utils
logger = logging.getLogger(__name__)


class ProductCategory(TimestampedModel):
    category_code = models.CharField(max_length=20, blank=True, null=True, unique=True)
    name = models.CharField(max_length=30)
    display_name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)

    class Meta:
        db_table = "product_category"
        verbose_name = "Product Category"
        verbose_name_plural = "Product Categories"

    def __str__(self):
        return self.name


def update_product_category_code(sender, instance, created, **kwargs):
    if created and not instance.category_code:
        instance.category_code = "C{0:06d}".format(instance.id)
        instance.save()


post_save.connect(update_product_category_code, sender=ProductCategory)


def upload_product_orig_image_path(instance, file):
    return "product/orig/{id}/{file}".format(id=instance.id, file=file)


def upload_product_thumb_image_path(instance, file):
    return "product/thumb/{id}/{file}".format(id=instance.id, file=file)


class Product(TimestampedModel):
    product_code = models.CharField(max_length=20, blank=True, null=True, unique=True)
    product_category = models.ForeignKey(ProductCategory)
    name = models.CharField(max_length=50)
    display_name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    img_orig = models.ImageField(upload_to=upload_product_orig_image_path, null=True, blank=True,
                                 storage=S3Boto3Storage(bucket=settings.AWS_STORAGE_PUBLIC_BUCKET_NAME))
    img_thumb = models.ImageField(upload_to=upload_product_thumb_image_path, null=True, blank=True,
                                  storage=S3Boto3Storage(bucket=settings.AWS_STORAGE_PUBLIC_BUCKET_NAME))

    class Meta:
        db_table = "product"
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def get_img_orig(self):
        if self.img_orig.name and utils.is_current_settings('production'):
            return utils.generate_public_s3_access_url(self.img_orig.name)
        return str(self.img_orig.name) if self.img_orig.name else ''

    def get_img_thumb(self):
        if self.img_thumb.name and utils.is_current_settings('production'):
            return utils.generate_public_s3_access_url(self.img_thumb.name)
        return str(self.img_thumb.name) if self.img_thumb.name else ''

    def __str__(self):
        return "{0} #{1}".format(self.product_category.name, self.name)


def update_product_code(sender, instance, created, **kwargs):
    if created and not instance.product_code:
        instance.product_code = "P{0:06d}".format(instance.id)
        instance.save()


post_save.connect(update_product_code, sender=Product)


def upload_sub_product_orig_image_path(instance, file):
    return "sub_product/orig/{id}/{file}".format(id=instance.id, file=file)


def upload_sub_product_thumb_image_path(instance, file):
    return "sub_product/thumb/{id}/{file}".format(id=instance.id, file=file)


class SubProduct(TimestampedModel):
    sub_product_code = models.CharField(max_length=20, blank=True, null=True, unique=True)
    product = models.ForeignKey(Product, related_name='sub_products')
    name = models.CharField(max_length=50)
    display_name = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    img_orig = models.ImageField(upload_to=upload_sub_product_orig_image_path, null=True, blank=True,
                                 storage=S3Boto3Storage(bucket=settings.AWS_STORAGE_PUBLIC_BUCKET_NAME))
    img_thumb = models.ImageField(upload_to=upload_sub_product_thumb_image_path, null=True, blank=True,
                                  storage=S3Boto3Storage(bucket=settings.AWS_STORAGE_PUBLIC_BUCKET_NAME))

    class Meta:
        db_table = "sub_product"
        verbose_name = "Sub Product"
        verbose_name_plural = "Sub products"

    def get_img_orig(self):
        if self.img_orig.name and utils.is_current_settings('production'):
            return utils.generate_public_s3_access_url(self.img_orig.name)
        return str(self.img_orig.name) if self.img_orig.name else ''

    def get_img_thumb(self):
        if self.img_thumb.name and utils.is_current_settings('production'):
            return utils.generate_public_s3_access_url(self.img_thumb.name)
        return str(self.img_thumb.name) if self.img_thumb.name else ''

    def __str__(self):
        return "{0} #{1} #{2}".format(self.product.product_category.name, self.product.name, self.name)


def update_sub_product_code(sender, instance, created, **kwargs):
    if created and not instance.sub_product_code:
        instance.sub_product_code = "SP{0:06d}".format(instance.id)
        instance.save()


post_save.connect(update_sub_product_code, sender=SubProduct)


class ProductDetail(TimestampedModel):
    product = models.ForeignKey(Product)
    key = models.CharField(max_length=50, blank=True, null=True)
    value = models.CharField(max_length=50)

    class Meta:
        db_table = "product_detail"
        verbose_name = "Product Detail"
        verbose_name_plural = "Product Details"
        unique_together = ('product', 'key')

    def __str__(self):
        return "{0}#{1}".format(self.key, self.value)
