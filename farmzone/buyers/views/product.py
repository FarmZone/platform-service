from .base import BaseAPIView, BaseModelViewSet
from rest_framework.response import Response
from farmzone.cms.product import get_buyer_products_summary, get_buyer_products_by_category, get_buyer_product_detail
from farmzone.settings.common import PAGINATION_DEFAULT_PER_PAGE_RECORD_COUNT
import logging
logger = logging.getLogger(__name__)


class BuyerProductsSummaryView(BaseAPIView):

    def get(self, request, user_id=None, app_version=None):
        seller = self.find_seller(user_id)
        logger.info("Processing Request to fetch products for user {0} & seller {1}".format(request.user.id, seller.seller_code))
        categories = get_buyer_products_summary(seller.seller_code)
        return Response({"categories": categories})


class BuyerProductsByCategoryView(BaseAPIView):

    def get(self, request, user_id=None, category_code=None, app_version=None):
        seller = self.find_seller(user_id)
        logger.info("Processing request to fetch product for user {0} with category code {1} and seller code {2}"
                    .format(self.request.user.id, category_code, seller.seller_code))

        # calculate the page and limit
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', PAGINATION_DEFAULT_PER_PAGE_RECORD_COUNT))
        offset = (page - 1) * page_size
        count = page_size * page
        #logger.debug("offset {0} and count {1}".format(offset, count))

        products = get_buyer_products_by_category(seller.seller_code, category_code, offset, count)
        return Response({"categories": products})


class BuyerProductDetailView(BaseAPIView):

    def get(self, request, user_id=None, product_code=None, app_version=None):
        seller = self.find_seller(user_id)
        logger.info("Processing request to fetch product detail for user {0} with product code {1} and seller code {2}"
                    .format(self.request.user.id, product_code, seller.seller_code))
        product_detail = get_buyer_product_detail(seller.seller_code, product_code)
        return Response({"categories": product_detail})
