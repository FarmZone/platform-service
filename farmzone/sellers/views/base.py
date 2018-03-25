from rest_framework.views import APIView
from farmzone.sellers.permissions import SellerPermission
from rest_framework import viewsets
from farmzone.util_config.custom_exceptions import CustomAPI404Exception
from farmzone.sellers.models import Seller
from farmzone.util_config.rest_customization import CustomPagination
import logging
logger = logging.getLogger(__name__)


class BaseAPIView(APIView):
    permission_classes = (SellerPermission, )

    def find_seller(self, seller_code=None):
        seller = Seller.find_seller(seller_code, self.request.user)
        if not seller:
            raise CustomAPI404Exception(
                {
                    "status_code": "INCORRECT_ID",
                    "details": "No record exists for specified seller_code"
                }
            )
        return seller


class BaseModelViewSet(viewsets.ModelViewSet):
    permission_classes = (SellerPermission, )
    pagination_class = CustomPagination
