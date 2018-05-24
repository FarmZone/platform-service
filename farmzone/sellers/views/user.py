from .base import BaseModelViewSet, BaseAPIView
from farmzone.ums.user import get_seller_preferred_users, get_seller_preferred_users_serializer, register_seller_device
from rest_framework.response import Response
from rest_framework import status
import logging
logger = logging.getLogger(__name__)


class SellerPreferredUserViewSet(BaseModelViewSet):
    serializer_class = get_seller_preferred_users_serializer()

    def get_queryset(self):
        user = self.request.user
        seller_code = self.kwargs.get('seller_code')
        return get_seller_preferred_users(seller_code)


class RegisterSellerDeviceView(BaseAPIView):

    def post(self, request, seller_code=None, app_version=None):
        user = self.request.user
        registration_id = request.data.get('registration_id')

        if not registration_id:
            logger.info("Mandatory fields missing. Requested params {0}".format(request.data))
            return Response({"details": "Registration id is missing.",
                             "status_code": "MISSING_REQUIRED_FIELDS"},
                            status.HTTP_200_OK)
        register_seller_device(user, seller_code, registration_id)
        return Response({"details": "User device registered successfully.",
                             "status_code": "SUCCESS"},
                            status.HTTP_200_OK)

