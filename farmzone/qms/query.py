from farmzone.support.models import Support, SupportStatus, SupportCategory
from farmzone.support.serializers import SupportSerializer
from farmzone.order.models import OrderDetail
from farmzone.util_config.custom_exceptions import CustomAPI400Exception
from farmzone.util_config.tasks import send_sms_to_user_id
from farmzone.notification.keys import query as keys
from django.db import transaction
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
            "details": "Given query_id is not a valid query id for this user",
            "status_code": "INVALID_REQUIRED_FIELDS"
        })
    if support.status != SupportStatus.ACCEPTED.value:
        logger.info("Support status is not in accepted state to resolve {0}".format(support.status))
        raise CustomAPI400Exception({
            "details": "Query is not in valid state of Accepted",
            "status_code": "INVALID_QUERY_STATE"
        })
    logger.info("Processing Request to resolve query for user {0}".format(user_id))
    with transaction.atomic():
        support.status = SupportStatus.RESOLVED.value
        support.save()


def accept_query(query_id, seller_code):
    support = Support.objects.filter(id=query_id,
                                     order_detail__seller_sub_product__seller__seller_code=seller_code).first()
    if not support:
        logger.info("query_id does not match any support query {0}".format(query_id))
        raise CustomAPI400Exception({
            "details": "Given query_id is not a valid query id for this user",
            "status_code": "INVALID_REQUIRED_FIELDS"
        })
    if support.status != SupportStatus.NEW.value:
        logger.info("Support status is not in New state to accept {0}".format(support.status))
        raise CustomAPI400Exception({
            "details": "Query is not in valid state of New",
            "status_code": "INVALID_QUERY_STATE"
        })
    logger.info("Processing Request to accept query for seller {0}".format(seller_code))
    with transaction.atomic():
        support.status = SupportStatus.ACCEPTED.value
        support.save()


def save_query(support_category_id, order_detail_id, user_id, support_status, comment):
    support_category = SupportCategory.objects.filter(id=support_category_id).first()
    if not support_category:
        logger.info("support_category_id does not match any support category {0}".format(support_category_id))
        raise CustomAPI400Exception({
            "details": "Please provide valid support_category_id parameter",
            "status_code": "INVALID_REQUIRED_FIELD"
        })
    order_detail = None
    if order_detail_id:
        order_detail = OrderDetail.objects.filter(id=order_detail_id).first()
        if not order_detail:
            logger.info("order_detail_id does not match any order_detail {0}".format(order_detail_id))
            raise CustomAPI400Exception({
                "details": "Please provide valid order_detail_id parameter",
                "status_code": "INVALID_PROVIDED_FIELD"
            })
    logger.info("Processing Request to add query for user {0}".format(user_id))
    with transaction.atomic():
        Support.add_query(user_id, order_detail, support_category, support_status, comment)
    send_sms_to_user_id(user_id, keys.buyer_save_query_buyer_key, order_detail_id=order_detail_id)