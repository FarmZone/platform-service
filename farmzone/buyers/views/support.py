from .base import BaseModelViewSet
from farmzone.qms.query import get_buyer_queries_with_status, get_buyer_queries_without_status\
    , get_support_queries_serializer
from farmzone.support.models import Support, SupportStatus
import logging
logger = logging.getLogger(__name__)


class BuyerPendingQueriesViewSet(BaseModelViewSet):
    serializer_class = get_support_queries_serializer()

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return get_buyer_queries_without_status(user_id, SupportStatus.RESOLVED.value)


class BuyerResolvedQueriesViewSet(BaseModelViewSet):
    serializer_class = get_support_queries_serializer()

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return get_buyer_queries_with_status(user_id, SupportStatus.RESOLVED.value)
