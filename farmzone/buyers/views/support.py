from .base import BaseModelViewSet, BaseAPIView
from farmzone.qms.query import get_buyer_queries_with_status, get_buyer_queries_without_status\
    , get_support_queries_serializer
from farmzone.support.models import Support, SupportStatus, SupportCategory
from farmzone.sellers.models import SellerSubProduct
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
        seller_sub_product_id = request.data.get('seller_sub_product_id')
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
        seller_sub_product = None
        if seller_sub_product_id:
            seller_sub_product = SellerSubProduct.objects.filter(id=seller_sub_product_id).first()
            if not seller_sub_product:
                logger.info("seller_sub_product_id does not match any seller_sub_product {0}".format(seller_sub_product_id))
                return Response({"details": "Please provide valid seller_sub_product_id parameter",
                                 "status_code": "INVALID_PROVIDED_FIELD"},
                                status.HTTP_400_BAD_REQUEST)

        logger.info("Processing Request to add query for user {0} & buyer {1}".format(request.user.id, user_id))
        Support.add_query(user, seller_sub_product, support_category, support_status, comment)
        return Response({"details": "Query added successfully",
                             "status_code": "SUCCESS"},
                            status.HTTP_200_OK)
