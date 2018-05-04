import logging
from farmzone.support.serializers import SupportCategorySerializer
from farmzone.support.models import SupportCategory
from farmzone.support.views.base import BaseModelViewSet

logger = logging.getLogger(__name__)


class SupportCategoryViewSet(BaseModelViewSet):
    serializer_class = SupportCategorySerializer

    def get_queryset(self):
        return SupportCategory.objects.exclude(id=999)
