from .base import BaseModelViewSet, BaseAPIView
from farmzone.ums.user import get_user_sellers, get_user_sellers_serializer, get_user_unassociated_sellers
from rest_framework.response import Response
import logging
logger = logging.getLogger(__name__)


class MySellersViewSet(BaseModelViewSet):
    serializer_class = get_user_sellers_serializer()

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return get_user_sellers(user_id)


class UnassociatedSellersView(BaseAPIView):
    def get(self, request, user_id=None, app_version=None):
        logger.info("Processing request to fetch unassociated sellers for user {0}".format(user_id))
        unassociated_sellers = get_user_unassociated_sellers(user_id)
        return Response({"sellers": unassociated_sellers})
