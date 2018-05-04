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
        support_status = SupportStatus.NEW.value
        if not support_category_id:
            logger.info("Manadatory fields missing. Requested params {0}".format(request.data))
            return Response({"details": "Please provide support_category_id parameter",
                             "status_code": "MISSING_REQUIRED_FIELDS"},
                            status.HTTP_400_BAD_REQUEST)
        save_query(support_category_id, order_detail_id, user_id, support_status, comment)
        return Response({"details": "Query added successfully",
                             "status_code": "SUCCESS"},
                            status.HTTP_200_OK)


class ResolveQueryView(BaseAPIView):

    def post(self, request, user_id=None, app_version=None):
        query_id = request.data.get('query_id')
        if not query_id:
            logger.info("Manadatory fields missing. Requested params {0}".format(request.data))
            return Response({"details": "Please provide query_id parameter",
                             "status_code": "MISSING_REQUIRED_FIELDS"},
                            status.HTTP_400_BAD_REQUEST)
        resolve_query(query_id, user_id)
        return Response({"details": "Query resolved successfully",
                             "status_code": "SUCCESS"},
                            status.HTTP_200_OK)
