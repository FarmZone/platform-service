import logging
from farmzone.support.serializers import SupportCategorySerializer
from farmzone.support.models import SupportCategory, SupportType
from farmzone.support.views.base import BaseModelViewSet

logger = logging.getLogger(__name__)


class SupportCategoryViewSet(BaseModelViewSet):
    serializer_class = SupportCategorySerializer

    def get_queryset(self):
        return SupportCategory.objects.filter(type=SupportType.QUERY.value).exclude(id=999)


class OrderSupportCategoryViewSet(BaseModelViewSet):
    serializer_class = SupportCategorySerializer

    def get_queryset(self):
        return SupportCategory.objects.filter(type=SupportType.ORDER.value).exclude(id=999)
