from farmzone.support.models import Support
from farmzone.support.serializers import SupportSerializer
import logging
logger = logging.getLogger(__name__)


def get_seller_queries_with_status(seller_code, query_status):
    return Support.objects.select_related('support_category').filter(seller_sub_product__seller__seller_code=seller_code) \
            .filter(status=query_status)


def get_seller_queries_without_status(seller_code, query_status):
    return Support.objects.select_related('support_category').filter(seller_sub_product__seller__seller_code=seller_code)\
            .exclude(status=query_status)


def get_support_queries_serializer():
    return SupportSerializer


def get_buyer_queries_with_status(user_id, query_status):
    return Support.objects.select_related('support_category').filter(user_id=user_id) \
            .filter(status=query_status)


def get_buyer_queries_without_status(user_id, query_status):
    return Support.objects.select_related('support_category').filter(user_id=user_id)\
            .exclude(status=query_status)