from .base import BaseAPIView
import logging
from rest_framework.response import Response
from farmzone.settings.common import PAGINATION_DEFAULT_PER_PAGE_RECORD_COUNT
from farmzone.oms.cart import get_cart_detail
from farmzone.oms.order import get_buyer_completed_orders, get_buyer_upcoming_orders

logger = logging.getLogger(__name__)


class CartDetailView(BaseAPIView):

    def get(self, request, user_id=None):
        logger.info("Processing Request to fetch cart for user {0} & buyer {1}".format(request.user.id, user_id))
        cart = get_cart_detail(user_id)
        return Response({"cart": cart})


class BuyerUpcomingOrdersView(BaseAPIView):

    def get(self, request, user_id=None):
        logger.info("Processing request to fetch upcoming orders for user {0} user_id {1}"
                    .format(self.request.user.id, user_id))

        # calculate the page and limit
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', PAGINATION_DEFAULT_PER_PAGE_RECORD_COUNT))
        offset = (page - 1) * page_size
        count = page_size * page
        #logger.debug("offset {0} and count {1}".format(offset, count))

        orders = get_buyer_upcoming_orders(user_id, offset, count)
        return Response({"orders": orders})


class BuyerCompletedOrdersView(BaseAPIView):

    def get(self, request, user_id=None):
        logger.info("Processing request to fetch completed orders for user {0} user_id {1}"
                    .format(self.request.user.id, user_id))

        # calculate the page and limit
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', PAGINATION_DEFAULT_PER_PAGE_RECORD_COUNT))
        offset = (page - 1) * page_size
        count = page_size * page
        #logger.debug("offset {0} and count {1}".format(offset, count))

        orders = get_buyer_completed_orders(user_id, offset, count)
        return Response({"orders": orders})
