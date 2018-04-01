from .base import BaseModelViewSet
from farmzone.ums.user import get_seller_preferred_users, get_seller_preferred_users_serializer
# from farmzone.ums.serializers import PreferredSellerSerializer
import logging
logger = logging.getLogger(__name__)


class SellerPreferredUserViewSet(BaseModelViewSet):
    serializer_class = get_seller_preferred_users_serializer()

    def get_queryset(self):
        user = self.request.user
        seller_code = self.kwargs.get('seller_code')
        return get_seller_preferred_users(seller_code)
