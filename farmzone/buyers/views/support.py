from .base import BaseModelViewSet, BaseAPIView
from farmzone.qms.query import get_buyer_queries_with_status, get_buyer_queries_without_status\
    , get_support_queries_serializer, resolve_query, save_query
from farmzone.support.models import SupportStatus
from rest_framework.response import Response
from rest_framework import status

import logging
logger = logging.getLogger(__name__)


class BuyerPendingQueriesViewSet(BaseModelViewSet):
    serializer_class = get_support_queries_serializer()

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return get_buyer_queries_without_status(user_id, SupportStatus.RESOLVED.value)


class BuyerResolvedQueriesViewSet(BaseModelViewSet):
    serializer_class = get_support_queries_serializer()

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return get_buyer_queries_with_status(user_id, SupportStatus.RESOLVED.value)


class SaveQueryView(BaseAPIView):

    def post(self, request, user_id=None, app_version=None):
        comment = request.data.get('comment')
        support_category_id = request.data.get('support_category_id')
        order_detail_id = request.data.get('order_detail_id')
        seller_code = request.data.get('seller_code')
        product_name = request.data.get('product_name')
        product_serial_no = request.data.get('product_serial_no')
        support_status = SupportStatus.NEW.value
        if not support_category_id:
            logger.info("Mandatory fields missing. Requested params {0}".format(request.data))
            return Response({"details": "Complain category id is missing.",
                             "status_code": "MISSING_REQUIRED_FIELDS"},
                            status.HTTP_200_OK)
        if not(seller_code or order_detail_id):
            logger.info("Mandatory fields missing. Requested params {0}".format(request.data))
            return Response({"details": "Either seller code or order item id is missing.",
                             "status_code": "MISSING_REQUIRED_FIELDS"},
                            status.HTTP_200_OK)
        save_query(support_category_id, order_detail_id, user_id, support_status, comment, seller_code, product_name, product_serial_no)
        return Response({"details": "Complain registered successfully.",
                             "status_code": "SUCCESS"},
                            status.HTTP_200_OK)


class ResolveQueryView(BaseAPIView):

    def post(self, request, user_id=None, app_version=None):
        query_id = request.data.get('query_id')
        if not query_id:
            logger.info("Mandatory fields missing. Requested params {0}".format(request.data))
            return Response({"details": "Complain id is missing.",
                             "status_code": "MISSING_REQUIRED_FIELDS"},
                            status.HTTP_200_OK)
        resolve_query(query_id, user_id)
        return Response({"details": "Complain marked resolved successfully.",
                             "status_code": "SUCCESS"},
                            status.HTTP_200_OK)
