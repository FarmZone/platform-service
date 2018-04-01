from rest_framework.views import APIView
from farmzone.buyers.permissions import BuyerPermission
from rest_framework import viewsets
from farmzone.util_config.custom_exceptions import CustomAPI404Exception
from farmzone.util_config.rest_customization import CustomPagination
import logging
logger = logging.getLogger(__name__)


class BaseAPIView(APIView):
    permission_classes = (BuyerPermission, )


class BaseModelViewSet(viewsets.ModelViewSet):
    permission_classes = (BuyerPermission, )
    pagination_class = CustomPagination
