import logging

from django.db import models
from farmzone.core.models import TimestampedModel, User
from farmzone.catalog.models import SubProduct
from django.db.models.signals import post_save

logger = logging.getLogger(__name__)


class Seller(TimestampedModel):
    seller_code = models.CharField(max_length=20, blank=True, null=True, unique=True)
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=False)

    class Meta:
        db_table = "sellers"
        verbose_name = "Seller"
        verbose_name_plural = "Sellers"

    def __str__(self):
        return self.name

    @staticmethod
    def find_seller(seller_code, user=None):
        if seller_code:
            return Seller.objects.get(seller_code=seller_code)
        logger.warning("No seller_code has been passed user: {0}".format(user))
        return Seller.get_seller_by_user(user)

    @staticmethod
    def get_seller_by_user(user):
        owner = SellerOwner.objects.select_related("seller").filter(user=user).first()
        return owner.seller if owner else None


def update_seller_code(sender, instance, created, **kwargs):
    if created and not instance.seller_code:
        instance.seller_code = "S{0:04d}".format(instance.id)
        instance.save()


post_save.connect(update_seller_code, sender=Seller)


class SellerOwner(TimestampedModel):
    user = models.ForeignKey(User)
    seller = models.ForeignKey(Seller)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "seller_owners"
        verbose_name = "Seller Owner"
        verbose_name_plural = "Seller Owners"
        unique_together = ('seller', 'user')

    def __str__(self):
        return self.user.full_name


class PreferredSeller(TimestampedModel):
    user = models.ForeignKey(User)
    seller = models.ForeignKey(Seller)

    class Meta:
        db_table = "preferred_seller"
        verbose_name = "Preferred Seller"
        verbose_name_plural = "Preferred Seller"
        unique_together = ('seller', 'user')

    def __str__(self):
        return self.user.full_name

    @classmethod
    def create_preferred_seller(cls, user, seller_code):
        preferred_seller = PreferredSeller.objects.filter(user=user).first()
        if preferred_seller:
            logger.info("preferred_seller already exist for user {0} ".format(user.id))
            return
        if not seller_code:
            logger.info("seller_code is not available in request for user {0} ".format(user.id))
            return
        seller_obj = Seller.objects.filter(seller_code=seller_code).first()
        if not seller_obj:
            logger.info("seller_code is not valid in request for user {0} ".format(user.id))
            return
        logger.info("Creating new preferred seller entry for user {0} ".format(user.id))
        PreferredSeller.objects.create(user=user, seller=seller_obj)


class SellerSubProduct(TimestampedModel):
    seller = models.ForeignKey(Seller)
    sub_product = models.ForeignKey(SubProduct, related_name='seller_sub_products')
    price = models.DecimalField(max_digits=8, decimal_places=2)
    discount = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    is_active = models.BooleanField(default=False)

    class Meta:
        db_table = "seller_sub_product"
        verbose_name = "Seller Sub Product"
        verbose_name_plural = "Seller Sub Products"

    def __str__(self):
        return "{0}#{1}".format(self.seller.name, self.sub_product)