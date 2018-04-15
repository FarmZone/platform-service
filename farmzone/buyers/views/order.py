from .base import BaseAPIView
import logging
from rest_framework.views import Response, status
from farmzone.settings.common import PAGINATION_DEFAULT_PER_PAGE_RECORD_COUNT
from farmzone.oms.order import get_buyer_completed_orders, get_buyer_upcoming_orders, place_order

logger = logging.getLogger(__name__)


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


class PlaceOrder(BaseAPIView):
    def post(self, request, user_id=None):
        data = request.data
        cart_id = data.get('id')

        if not cart_id:
            logger.info("Manadatory fields missing. Requested params {0}".format(data))
            return Response({"details": "Please provide id parameter",
                             "status_code": "MISSING_REQUIRED_FIELDS"},
                            status.HTTP_404_NOT_FOUND)
        logger.info("Processing Request to place order for user {0} & buyer {1}".format(request.user.id, user_id))
        place_order(user_id, cart_id)
        return Response({"details": "Order placed successfully",
                             "status_code": "SUCCESS"},
                            status.HTTP_200_OK)