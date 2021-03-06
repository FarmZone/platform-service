from .base import BaseAPIView
import logging
from rest_framework.views import Response, status
from farmzone.oms.cart import get_cart_detail, add_to_cart

logger = logging.getLogger(__name__)


class CartDetailView(BaseAPIView):

    def get(self, request, user_id=None, app_version=None):
        logger.info("Processing Request to fetch cart for user {0} & buyer {1}".format(request.user.id, user_id))
        cart = get_cart_detail(user_id)
        return Response({"cart": cart})


class AddToCartView(BaseAPIView):

    def post(self, request, user_id=None, app_version=None):
        data = request.data
        seller_sub_product_id = data.get('seller_sub_product_id')
        qty = data.get('qty')

        if not seller_sub_product_id or qty is None:
            logger.info("Mandatory fields missing. Requested params {0}".format(data))
            return Response({"details": "Either qty or seller sub product id is missing.",
                             "status_code": "MISSING_REQUIRED_FIELDS"},
                            status.HTTP_200_OK)
        if not (isinstance(qty, int) and qty >= 0):
            return Response({"details": "Qty must be zero or greater than zero.",
                             "status_code": "INVALID_REQUIRED_FIELDS"},
                            status.HTTP_200_OK)
        logger.info("Processing Request to add item in cart for user {0} & buyer {1}".format(request.user.id, user_id))
        add_to_cart(user_id, seller_sub_product_id, qty)
        return Response({"details": "Cart updated successfully.",
                             "status_code": "SUCCESS"},
                            status.HTTP_200_OK)

