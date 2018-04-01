from .base import BaseAPIView
from farmzone.oms.order import get_seller_upcoming_orders, get_seller_completed_orders
import logging
from rest_framework.response import Response
from farmzone.settings.common import PAGINATION_DEFAULT_PER_PAGE_RECORD_COUNT
logger = logging.getLogger(__name__)


class SellerUpcomingOrdersView(BaseAPIView):

    def get(self, request, seller_code=None):
        logger.info("Processing request to fetch upcoming orders for user {0} seller code {1}"
                    .format(self.request.user.id, seller_code))

        # calculate the page and limit
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', PAGINATION_DEFAULT_PER_PAGE_RECORD_COUNT))
        offset = (page - 1) * page_size
        count = page_size * page
        #logger.debug("offset {0} and count {1}".format(offset, count))

        orders = get_seller_upcoming_orders(seller_code, offset, count)
        return Response({"orders": orders})


class SellerCompletedOrdersView(BaseAPIView):

    def get(self, request, seller_code=None):
        logger.info("Processing request to fetch completed orders for user {0} seller code {1}"
                    .format(self.request.user.id, seller_code))

        # calculate the page and limit
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', PAGINATION_DEFAULT_PER_PAGE_RECORD_COUNT))
        offset = (page - 1) * page_size
        count = page_size * page
        #logger.debug("offset {0} and count {1}".format(offset, count))

        orders = get_seller_completed_orders(seller_code, offset, count)
        return Response({"orders": orders})
