import logging
from django.db import transaction
from farmzone.oms.order import get_cart_product_detail
from farmzone.order.models import OrderDetail, Orders, OrderStatus
from farmzone.sellers.models import SellerSubProduct
from farmzone.util_config.custom_exceptions import CustomAPI400Exception
logger = logging.getLogger(__name__)


def get_cart_detail(user_id):
    # seller_subproduct_ids = ",".join(map(str, Cart.objects.filter(user_id=user_id).values_list('seller_sub_product_id', flat=True)))
    # logger.debug("seller_subproduct_ids {0}".format(seller_subproduct_ids))
    cart = get_cart_product_detail(user_id)
    return cart


def add_to_cart(user_id, seller_sub_product_id, qty):
    seller_sub_product = SellerSubProduct.objects.filter(id=seller_sub_product_id, is_active=True,
                                                         seller__is_active=True).first()
    if not seller_sub_product:
        raise CustomAPI400Exception({
            "details": "Seller_sub_product_id is either not active or does not exist",
            "status_code": "INVALID_REQUIRED_FIELDS"
        })

    with transaction.atomic():
        order_detail = OrderDetail.objects.select_related("order").filter(status=OrderStatus.CART.value, order__user_id=user_id).first()
        if not order_detail:
            if qty == 0:
                raise CustomAPI400Exception({
                    "details": "qty parameter can not be zero",
                    "status_code": "INVALID_REQUIRED_FIELDS"
                })
            order_created = create_cart(user_id)
            order_detail_created = create_cart_detail(order_created, seller_sub_product, qty)
        else:
            order_detail_sub_product = OrderDetail.objects.select_related("order")\
                .filter(status=OrderStatus.CART.value, order=order_detail.order, seller_sub_product_id=seller_sub_product_id).first()
            if not order_detail_sub_product:
                if qty == 0:
                    raise CustomAPI400Exception({
                        "details": "qty parameter can not be zero",
                        "status_code": "INVALID_REQUIRED_FIELDS"
                    })
                order_detail_created = create_cart_detail(order_detail.order, seller_sub_product, qty)
            else:
                if qty != 0:
                    order_detail_updated = update_cart_detail(order_detail.order, seller_sub_product, qty)
                else:
                    delete_cart_detail(order_detail.order, seller_sub_product, qty)
        # cart = get_cart_product_detail(user_id)
        # return cart


def create_cart(user_id):
    return Orders.objects.create(total_price=0, user_id=user_id)


def create_cart_detail(order, seller_sub_product, qty):
    return OrderDetail.objects.create(price=seller_sub_product.price, discount=seller_sub_product.discount
                               , qty=qty, status=OrderStatus.CART.value, order=order, seller_sub_product=seller_sub_product)


def update_cart_detail(order, seller_sub_product, qty):
    return OrderDetail.objects.filter(status=OrderStatus.CART.value, order=order, seller_sub_product=seller_sub_product)\
        .update(price=seller_sub_product.price, discount=seller_sub_product.discount, qty=qty)


def delete_cart_detail(order, seller_sub_product, qty):
    OrderDetail.objects.filter(status=OrderStatus.CART.value, order=order, seller_sub_product=seller_sub_product).delete()
    order_detail_count = OrderDetail.objects.filter(status=OrderStatus.CART.value, order=order).count()
    if order_detail_count == 0:
        order.delete()