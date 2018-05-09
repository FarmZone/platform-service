from rest_framework.views import APIView
from farmzone.buyers.permissions import BuyerPermission
from rest_framework import viewsets
from farmzone.util_config.custom_exceptions import CustomAPI404Exception
from farmzone.util_config.rest_customization import CustomPagination
from farmzone.ums.user import get_seller_by_user
import logging
logger = logging.getLogger(__name__)


class BaseAPIView(APIView):
    permission_classes = (BuyerPermission, )

    def find_seller(self, user_id=None):
        seller = get_seller_by_user(user_id)
        if not seller:
            raise CustomAPI404Exception(
                {
                    "status_code": "NO_SELLER_ASSOCIATED",
                    "details": "We could not find any seller associated with you."
                }
            )
        return seller


class BaseModelViewSet(viewsets.ModelViewSet):
    permission_classes = (BuyerPermission, )
    pagination_class = CustomPagination
