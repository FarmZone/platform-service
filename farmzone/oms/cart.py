import logging
from farmzone.order.models import Cart
from farmzone.cms.product import get_cart_product_detail
logger = logging.getLogger(__name__)


def get_cart_detail(user_id):
    seller_subproduct_ids = ",".join(map(str, Cart.objects.filter(user_id=user_id).values_list('seller_sub_product_id', flat=True)))
    logger.debug("seller_subproduct_ids {0}".format(seller_subproduct_ids))
    cart = get_cart_product_detail(seller_subproduct_ids)
    return cart