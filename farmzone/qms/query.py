from farmzone.support.models import Support
from farmzone.support.serializers import SupportSerializer
import logging
logger = logging.getLogger(__name__)


def get_seller_queries_with_status(seller_code, query_status):
    return Support.objects.select_related('support_category').filter(seller__seller_code=seller_code) \
            .filter(status=query_status)


def get_seller_queries_without_status(seller_code, query_status):
    return Support.objects.select_related('support_category').filter(seller__seller_code=seller_code)\
            .exclude(status=query_status)


def get_seller_queries_serializer():
    return SupportSerializer
