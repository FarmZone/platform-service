from .base import BaseModelViewSet
from farmzone.qms.query import get_seller_queries_without_status, get_seller_queries_with_status\
    , get_support_queries_serializer
from farmzone.support.models import Support, SupportStatus
import logging
logger = logging.getLogger(__name__)


class SellerPendingQueriesViewSet(BaseModelViewSet):
    serializer_class = get_support_queries_serializer()

    def get_queryset(self):
        seller_code = self.kwargs.get('seller_code')
        return get_seller_queries_without_status(seller_code, SupportStatus.RESOLVED.value)


class SellerResolvedQueriesViewSet(BaseModelViewSet):
    serializer_class = get_support_queries_serializer()

    def get_queryset(self):
        seller_code = self.kwargs.get('seller_code')
        return get_seller_queries_with_status(seller_code, SupportStatus.RESOLVED.value)
