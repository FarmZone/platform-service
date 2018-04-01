from .base import BaseModelViewSet
from farmzone.ums.user import get_seller_preferred_users, get_seller_preferred_users_serializer
from farmzone.support.models import Support, SupportStatus
import logging
logger = logging.getLogger(__name__)


class SellerPendingQueriesViewSet(BaseModelViewSet):
    serializer_class = get_seller_preferred_users_serializer()

    def get_queryset(self):
        seller_code = self.kwargs.get('seller_code')
        return Support.objects.select_related('support_category').filter(seller__seller_code=seller_code)\
            .exclude(status=SupportStatus.COMPLETED.value)


class SellerResolvedQueriesViewSet(BaseModelViewSet):
    serializer_class = get_seller_preferred_users_serializer()

    def get_queryset(self):
        seller_code = self.kwargs.get('seller_code')
        return Support.objects.select_related('support_category').filter(seller__seller_code=seller_code) \
            .filter(status=SupportStatus.COMPLETED.value)
