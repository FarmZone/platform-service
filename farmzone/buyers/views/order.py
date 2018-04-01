from .base import BaseAPIView
import logging
from rest_framework.response import Response
from farmzone.oms.cart import get_cart_detail

logger = logging.getLogger(__name__)


class CartDetailView(BaseAPIView):

    def get(self, request, user_id=None):
        logger.info("Processing Request to fetch cart for user {0} & buyer {1}".format(request.user.id, user_id))
        cart = get_cart_detail(user_id)
        return Response({"cart": cart})


class OrderView(BaseAPIView):
    pass
    # def get(self, request, user_id=None):
    #     logger.info("Processing Request to fetch cart for user {0} & buyer {1}".format(request.user.id, user_id))
    #     cart = get_cart_detail(user_id)
    #     return Response({"cart": cart})


class OrderDetailView(BaseAPIView):
    pass
    # def get(self, request, user_id=None):
    #     logger.info("Processing Request to fetch cart for user {0} & buyer {1}".format(request.user.id, user_id))
    #     cart = get_cart_detail(user_id)
    #     return Response({"cart": cart})
