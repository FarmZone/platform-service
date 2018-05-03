from rest_framework import viewsets
from farmzone.util_config.rest_customization import CustomPagination
import logging
logger = logging.getLogger(__name__)


class BaseModelViewSet(viewsets.ModelViewSet):
    permission_classes = ()
    pagination_class = CustomPagination
