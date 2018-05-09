from .base import BaseModelViewSet, BaseAPIView
from farmzone.ums.user import get_user_sellers, get_user_sellers_serializer, get_user_unassociated_sellers, add_seller
from rest_framework.views import Response, status
import logging
logger = logging.getLogger(__name__)


class MySellersViewSet(BaseModelViewSet):
    serializer_class = get_user_sellers_serializer()

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return get_user_sellers(user_id)


class UnassociatedSellersView(BaseAPIView):
    def get(self, request, user_id=None, app_version=None):
        q = request.GET.get('q')
        if not q:
            return Response({"sellers": []})
        unassociated_sellers = get_user_unassociated_sellers(user_id, q)
        return Response({"sellers": unassociated_sellers})


class AddSellerView(BaseAPIView):
    def post(self, request, user_id=None, app_version=None):
        seller_code = request.data.get('seller_code')
        if not seller_code:
            logger.info("Manadatory fields missing. Requested params {0}".format(request.data))
            return Response({"details": "Please provide seller_code parameter",
                             "status_code": "MISSING_REQUIRED_FIELDS"},
                            status.HTTP_200_OK)
        add_seller(seller_code, user_id)
        return Response({"details": "Seller added successfully",
                         "status_code": "SUCCESS"},
                        status.HTTP_200_OK)
