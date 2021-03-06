from .base import BaseAPIView
import logging
from rest_framework.views import Response, status
from farmzone.settings.common import PAGINATION_DEFAULT_PER_PAGE_RECORD_COUNT
from farmzone.oms.order import get_buyer_completed_orders, get_buyer_upcoming_orders, place_order\
    , cancel_order, save_order_rating, complete_order

logger = logging.getLogger(__name__)


class BuyerUpcomingOrdersView(BaseAPIView):

    def get(self, request, user_id=None, app_version=None):
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

    def get(self, request, user_id=None, app_version=None):
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
    def post(self, request, user_id=None, app_version=None):
        data = request.data
        cart_id = data.get('id')

        if not cart_id:
            logger.info("Mandatory fields missing. Requested params {0}".format(data))
            return Response({"details": "Cart id is missing.",
                             "status_code": "MISSING_REQUIRED_FIELDS"},
                            status.HTTP_200_OK)
        logger.info("Processing Request to place order for user {0} & buyer {1}".format(request.user.id, user_id))
        place_order(user_id, cart_id)
        return Response({"details": "Order placed successfully.",
                             "status_code": "SUCCESS"},
                            status.HTTP_200_OK)


class CancelOrder(BaseAPIView):
    def post(self, request, user_id=None, app_version=None):
        data = request.data
        order_id = data.get('id')

        if not order_id:
            logger.info("Mandatory fields missing. Requested params {0}".format(data))
            return Response({"details": "Order id is missing.",
                             "status_code": "MISSING_REQUIRED_FIELDS"},
                            status.HTTP_200_OK)
        logger.info("Processing Request to cancel order for user {0} & buyer {1}".format(request.user.id, user_id))
        cancel_order(user_id, order_id)
        return Response({"details": "Order cancelled successfully.",
                             "status_code": "SUCCESS"},
                            status.HTTP_200_OK)


class SaveOrderRatingView(BaseAPIView):

    def post(self, request, user_id=None, app_version=None):
        rating = request.data.get('rating')
        order_detail_id = request.data.get('order_detail_id')
        if not order_detail_id or not rating:
            logger.info("Mandatory fields missing. Requested params {0}".format(request.data))
            return Response({"details": "Either rating or order item id is missing.",
                             "status_code": "MISSING_REQUIRED_FIELDS"},
                            status.HTTP_200_OK)
        save_order_rating(order_detail_id, rating, user_id)
        return Response({"details": "Rating saved successfully.",
                             "status_code": "SUCCESS"},
                            status.HTTP_200_OK)


class CompleteOrderView(BaseAPIView):

    def post(self, request, user_id=None, app_version=None):
        order_detail_id = request.data.get('order_detail_id')
        product_identifiers = request.data.get('product_identifiers')
        if not order_detail_id:
            logger.info("Mandatory fields missing. Requested params {0}".format(request.data))
            return Response({"details": "Order item id is missing.",
                             "status_code": "MISSING_REQUIRED_FIELDS"},
                            status.HTTP_200_OK)
        if not product_identifiers:
            logger.info("Mandatory fields missing. Requested params {0}".format(request.data))
            return Response({"details": "Product unique id is missing.",
                             "status_code": "MISSING_REQUIRED_FIELDS"},
                            status.HTTP_200_OK)
        product_identifiers_set = set(product_identifiers)
        if len(product_identifiers)!= len(product_identifiers_set):
            logger.info("Duplicate product identifiers. Requested params {0}".format(request.data))
            return Response({"details": "Product id already exists. Please provide unique id.",
                             "status_code": "DUPLICATE_REQUIRED_FIELDS"},
                            status.HTTP_200_OK)
        complete_order(order_detail_id, user_id, product_identifiers)
        return Response({"details": "Order marked delivered successfully.",
                             "status_code": "SUCCESS"},
                            status.HTTP_200_OK)
