from .base import BaseModelViewSet, BaseAPIView
from farmzone.qms.query import get_buyer_queries_with_status, get_buyer_queries_without_status\
    , get_support_queries_serializer
from farmzone.support.models import Support, SupportStatus, SupportCategory
from farmzone.sellers.models import SellerSubProduct
from farmzone.order.models import OrderDetail
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
        user = request.user
        if not support_category_id:
            logger.info("Manadatory fields missing. Requested params {0}".format(request.data))
            return Response({"details": "Please provide support_category_id parameter",
                             "status_code": "MISSING_REQUIRED_FIELDS"},
                            status.HTTP_400_BAD_REQUEST)
        support_category = SupportCategory.objects.filter(id=support_category_id).first()
        if not support_category:
            logger.info("support_category_id does not match any support category {0}".format(support_category_id))
            return Response({"details": "Please provide valid support_category_id parameter",
                             "status_code": "INVALID_REQUIRED_FIELD"},
                            status.HTTP_400_BAD_REQUEST)
        order_detail = None
        if order_detail_id:
            order_detail = OrderDetail.objects.filter(id=order_detail_id).first()
            if not order_detail:
                logger.info("order_detail_id does not match any order_detail {0}".format(order_detail_id))
                return Response({"details": "Please provide valid order_detail_id parameter",
                                 "status_code": "INVALID_PROVIDED_FIELD"},
                                status.HTTP_400_BAD_REQUEST)

        logger.info("Processing Request to add query for user {0} & buyer {1}".format(request.user.id, user_id))
        Support.add_query(user, order_detail, support_category, support_status, comment)
        return Response({"details": "Query added successfully",
                             "status_code": "SUCCESS"},
                            status.HTTP_200_OK)


class ResolveQueryView(BaseAPIView):

    def post(self, request, user_id=None, app_version=None):
        query_id = request.data.get('query_id')
        user = request.user
        if not query_id:
            logger.info("Manadatory fields missing. Requested params {0}".format(request.data))
            return Response({"details": "Please provide query_id parameter",
                             "status_code": "MISSING_REQUIRED_FIELDS"},
                            status.HTTP_400_BAD_REQUEST)
        support = Support.objects.filter(id=query_id, user=user).first()
        if not support:
            logger.info("query_id does not match any support query {0}".format(query_id))
            return Response({"details": "Please provide valid query_id parameter",
                             "status_code": "INVALID_REQUIRED_FIELD"},
                            status.HTTP_400_BAD_REQUEST)
        if support.status != SupportStatus.ACCEPTED.value:
            logger.info("Support status is not in accepted state to resolve {0}".format(support.status))
            return Response({"details": "Query is not in valid state of Accepted",
                                 "status_code": "INVALID_QUERY_STATE"},
                                status.HTTP_400_BAD_REQUEST)

        logger.info("Processing Request to resolve query for user {0} & buyer {1}".format(request.user.id, user_id))
        support.status = SupportStatus.RESOLVED.value
        support.save()
        return Response({"details": "Query resolved successfully",
                             "status_code": "SUCCESS"},
                            status.HTTP_200_OK)
