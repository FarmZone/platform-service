from .base import BaseModelViewSet, BaseAPIView
from farmzone.qms.query import get_seller_queries_without_status, get_seller_queries_with_status\
    , get_support_queries_serializer, accept_query
from farmzone.support.models import SupportStatus
from rest_framework.response import Response
from rest_framework import status

import logging
logger = logging.getLogger(__name__)


class SellerPendingQueriesViewSet(BaseModelViewSet):
    serializer_class = get_support_queries_serializer()

    def get_queryset(self):
        seller_code = self.kwargs.get('seller_code')
        return get_seller_queries_without_status(seller_code, SupportStatus.RESOLVED.value)


class SellerResolvedQueriesViewSet(BaseModelViewSet):
    serializer_class = get_support_queries_serializer()

    def get_queryset(self):
        seller_code = self.kwargs.get('seller_code')
        return get_seller_queries_with_status(seller_code, SupportStatus.RESOLVED.value)


class AcceptQueryView(BaseAPIView):

    def post(self, request, seller_code=None, app_version=None):
        query_id = request.data.get('query_id')
        if not query_id:
            logger.info("Manadatory fields missing. Requested params {0}".format(request.data))
            return Response({"details": "Please provide query_id parameter",
                             "status_code": "MISSING_REQUIRED_FIELDS"},
                            status.HTTP_200_OK)
        accept_query(query_id, seller_code)
        return Response({"details": "Query accepted successfully",
                             "status_code": "SUCCESS"},
                            status.HTTP_200_OK)

