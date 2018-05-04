import logging
from django.db import models
from farmzone.core.models import TimestampedModel, User
from farmzone.sellers.models import SellerSubProduct
from farmzone.util_config import ModelEnum
logger = logging.getLogger(__name__)


# class Cart(TimestampedModel):
#     user = models.ForeignKey(User)
#     seller_sub_product = models.ForeignKey(SellerSubProduct)
#     price = models.DecimalField(max_digits=8, decimal_places=2)
#     discount = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
#     qty = models.IntegerField(default=0)
#
#     class Meta:
#         db_table = "cart"
#         verbose_name = "Cart"
#         verbose_name_plural = "Cart"
#
#     def __str__(self):
#         return "{0}# {1}#".format(self.user_id, self.seller_sub_product)


class Orders(TimestampedModel):
    user = models.ForeignKey(User)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        db_table = "orders"
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return "{0}# {1}#".format(self.id, self.user)


class OrderStatus(ModelEnum):
    NEW = "NEW"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    COMPLETED = "COMPLETED"
    CART = "CART"
    CANCELLED = "CANCELLED"


ORDER_CANCELLED_STATUS = [
    OrderStatus.NEW.value,
    OrderStatus.ACCEPTED.value
]


class OrderDetail(TimestampedModel):
    order = models.ForeignKey(Orders, related_name='order_detail')
    seller_sub_product = models.ForeignKey(SellerSubProduct)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    discount = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    qty = models.IntegerField(default=0)
    status = models.CharField(choices=OrderStatus.get_values(), max_length=30, default=OrderStatus.NEW.value)
    rating = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    class Meta:
        db_table = "order_detail"
        verbose_name = "Order Detail"
        verbose_name_plural = "Order Details"

    def __str__(self):
        return "{0}# {1}#".format(self.order, self.seller_sub_product)


