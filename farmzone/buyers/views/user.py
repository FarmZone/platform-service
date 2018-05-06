from .base import BaseModelViewSet
from farmzone.ums.user import get_user_sellers, get_user_sellers_serializer
import logging
logger = logging.getLogger(__name__)


class MySellersViewSet(BaseModelViewSet):
    serializer_class = get_user_sellers_serializer()

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return get_user_sellers(user_id)
