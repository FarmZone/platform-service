import logging
from django.db import models
from farmzone.core.models import TimestampedModel, User
from farmzone.sellers.models import SellerSubProduct
from farmzone.util_config import ModelEnum
from django.db.models.signals import post_save
logger = logging.getLogger(__name__)


class SupportCategory(TimestampedModel):
    category_code = models.CharField(max_length=20, blank=True, null=True, unique=True)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=200)

    class Meta:
        db_table = "support_category"
        verbose_name = "Support Category"
        verbose_name_plural = "Support Categories"

    def __str__(self):
        return self.name


def update_support_category_code(sender, instance, created, **kwargs):
    if created and not instance.category_code:
        instance.category_code = "C{0:02d}".format(instance.id)
        instance.save()


post_save.connect(update_support_category_code, sender=SupportCategory)


class SupportStatus(ModelEnum):
    NEW = "NEW"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    RESOLVED = "RESOLVED"


class Support(TimestampedModel):
    support_category = models.ForeignKey(SupportCategory)
    seller_sub_product = models.ForeignKey(SellerSubProduct, blank=True, null=True)
    user = models.ForeignKey(User)
    comment = models.CharField(max_length=500)
    status = models.CharField(choices=SupportStatus.get_values(), max_length=30, default=SupportStatus.NEW.value)

    class Meta:
        db_table = "support"
        verbose_name = "Support"
        verbose_name_plural = "Supports"

    def __str__(self):
        return "{0} #{1}".format(self.support_category.name, self.user.full_name)
