from .base import BaseModelViewSet, BaseAPIView
from farmzone.qms.query import get_seller_queries_without_status, get_seller_queries_with_status\
    , get_support_queries_serializer
from farmzone.support.models import Support, SupportStatus
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
        user = request.user
        if not query_id:
            logger.info("Manadatory fields missing. Requested params {0}".format(request.data))
            return Response({"details": "Please provide query_id parameter",
                             "status_code": "MISSING_REQUIRED_FIELDS"},
                            status.HTTP_400_BAD_REQUEST)
        support = Support.objects.filter(id=query_id, order_detail__seller_sub_product__seller__seller_code=seller_code).first()
        if not support:
            logger.info("query_id does not match any support query {0}".format(query_id))
            return Response({"details": "Please provide valid query_id parameter",
                             "status_code": "INVALID_REQUIRED_FIELD"},
                            status.HTTP_400_BAD_REQUEST)
        if support.status != SupportStatus.NEW.value:
            logger.info("Support status is not in New state to accept {0}".format(support.status))
            return Response({"details": "Query is not in valid state of New",
                                 "status_code": "INVALID_QUERY_STATE"},
                                status.HTTP_400_BAD_REQUEST)

        logger.info("Processing Request to accept query for user {0} & seller {1}".format(request.user.id, seller_code))
        support.status = SupportStatus.ACCEPTED.value
        support.save()
        return Response({"details": "Query accepted successfully",
                             "status_code": "SUCCESS"},
                            status.HTTP_200_OK)

