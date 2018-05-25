from farmzone.support.models import Support, SupportStatus, SupportCategory
from farmzone.support.serializers import SupportSerializer
from farmzone.order.models import OrderDetail
from farmzone.sellers.models import Seller, SellerOwner
from farmzone.util_config.custom_exceptions import CustomAPI400Exception
from farmzone.notification import notification

from django.db import transaction
from django.db.models import Q
import logging
logger = logging.getLogger(__name__)


def get_seller_queries_with_status(seller_code, query_status):
    return Support.objects.select_related('support_category').filter(order_detail__seller_sub_product__seller__seller_code=seller_code) \
            .filter(status=query_status)


def get_seller_queries_without_status(seller_code, query_status):
    return Support.objects.select_related('support_category').filter(order_detail__seller_sub_product__seller__seller_code=seller_code)\
            .exclude(status=query_status)


def get_support_queries_serializer():
    return SupportSerializer


def get_buyer_queries_with_status(user_id, query_status):
    return Support.objects.select_related('support_category').filter(user_id=user_id) \
            .filter(status=query_status)


def get_buyer_queries_without_status(user_id, query_status):
    return Support.objects.select_related('support_category').filter(user_id=user_id)\
            .exclude(status=query_status)


def resolve_query(query_id, user_id):
    support = Support.objects.filter(id=query_id, user_id=user_id).first()
    if not support:
        logger.info("query_id does not match any support query {0}".format(query_id))
        raise CustomAPI400Exception({
            "details": "Complain id is not valid.",
            "status_code": "INVALID_REQUIRED_FIELDS"
        })
    if support.status != SupportStatus.ACCEPTED.value:
        logger.info("Support status is not in accepted state to resolve {0}".format(support.status))
        raise CustomAPI400Exception({
            "details": "Complain is not in accepted state.",
            "status_code": "INVALID_QUERY_STATE"
        })
    logger.info("Processing Request to resolve query for user {0}".format(user_id))
    with transaction.atomic():
        support.status = SupportStatus.RESOLVED.value
        support.save()
    seller_user = get_seller_user_by_query(query_id)
    notification.send_resolve_query_notification(user_id, query_id, seller_user)


def accept_query(query_id, seller_code):
    support = Support.objects.filter(id=query_id).filter(seller__seller_code=seller_code).first()
    if not support:
        logger.info("query_id does not match any support query {0}".format(query_id))
        raise CustomAPI400Exception({
            "details": "Complain id is not valid.",
            "status_code": "INVALID_REQUIRED_FIELDS"
        })
    if support.status != SupportStatus.NEW.value:
        logger.info("Support status is not in New state to accept {0}".format(support.status))
        raise CustomAPI400Exception({
            "details": "Complain is not in new state.",
            "status_code": "INVALID_QUERY_STATE"
        })
    logger.info("Processing Request to accept query for seller {0}".format(seller_code))
    with transaction.atomic():
        support.status = SupportStatus.ACCEPTED.value
        support.save()
    seller_user = get_seller_user_by_query(query_id)
    buyer_user = get_buyer_user_by_query(query_id)
    notification.send_accept_query_notification(query_id, buyer_user, seller_user)


def save_query(support_category_id, order_detail_id, user_id, support_status, comment, seller_code, product_name, product_serial_no):
    support_category = SupportCategory.objects.filter(id=support_category_id).first()
    if not support_category:
        logger.info("support_category_id does not match any support category {0}".format(support_category_id))
        raise CustomAPI400Exception({
            "details": "Complain category id is not valid.",
            "status_code": "INVALID_REQUIRED_FIELD"
        })
    order_detail = None
    seller = None
    if order_detail_id:
        order_detail = OrderDetail.objects.filter(id=order_detail_id).select_related('seller_sub_product', 'seller_sub_product__seller').first()
        if not order_detail:
            logger.info("order_detail_id does not match any order_detail {0}".format(order_detail_id))
            raise CustomAPI400Exception({
                "details": "Order detail id is not valid.",
                "status_code": "INVALID_PROVIDED_FIELD"
            })
        seller = order_detail.seller_sub_product.seller
    if seller_code:
        seller = Seller.objects.filter(seller_code=seller_code).first()
        if not seller:
            logger.info("seller_code does not match any seller {0}".format(seller_code))
            raise CustomAPI400Exception({
                "details": "Seller code is not valid.",
                "status_code": "INVALID_PROVIDED_FIELD"
            })
        if not product_name:
            logger.info("product_name is mandatory if seller {0} given".format(seller_code))
            raise CustomAPI400Exception({
                "details": "Product name is missing.",
                "status_code": "INVALID_REQUIRED_FIELD"
            })
    logger.info("Processing Request to add query for user {0}".format(user_id))
    with transaction.atomic():
        support = Support.add_query(user_id, order_detail, support_category, support_status, comment, seller, product_name, product_serial_no)
        seller_user = get_seller_user_by_query(support.id)
        notification.send_save_query_notification(user_id, support.id, seller_user)


def get_seller_user_by_query(query_id):
    support = Support.objects.select_related("order_detail", "seller").filter(id=query_id).first()
    if support:
        seller = support.seller if support.seller \
            else support.order_detail.seller_sub_product.seller if support.order_detail else None
        if seller:
            seller_owner = SellerOwner.objects.select_related("user").filter(seller=seller).first()
            if seller_owner:
                return seller_owner.user
    return None


def get_buyer_user_by_query(query_id):
    support = Support.objects.select_related("user").filter(id=query_id).first()
    if support:
        return support.user
    return None
