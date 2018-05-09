from .base import BaseAPIView, BaseModelViewSet
from rest_framework.response import Response
from farmzone.cms.product import get_buyer_products_summary, get_buyer_products_by_category\
    , get_buyer_product_detail, add_user_product, get_user_products, get_user_products_serializer, update_user_product
from farmzone.settings.common import PAGINATION_DEFAULT_PER_PAGE_RECORD_COUNT
from rest_framework.views import Response, status
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


class AddMyProduct(BaseAPIView):
    def post(self, request, user_id=None, app_version=None):
        seller_code = request.data.get('seller_code')
        product_name = request.data.get('product_name')
        product_serial_no = request.data.get('product_serial_no')
        if not seller_code or not product_name or not product_serial_no:
            logger.info("Manadatory fields missing. Requested params {0}".format(request.data))
            return Response({"details": "Either seller code or product name or product id is missing.",
                             "status_code": "MISSING_REQUIRED_FIELDS"},
                            status.HTTP_200_OK)
        add_user_product(seller_code, product_name, product_serial_no, user_id)
        return Response({"details": "Product added successfully.",
                         "status_code": "SUCCESS"},
                        status.HTTP_200_OK)


class UpdateMyProduct(BaseAPIView):
    def post(self, request, user_id=None, app_version=None):
        id = request.data.get('id')
        seller_code = request.data.get('seller_code')
        product_name = request.data.get('product_name')
        product_serial_no = request.data.get('product_serial_no')
        if not id or not seller_code or not product_name or not product_serial_no:
            logger.info("Manadatory fields missing. Requested params {0}".format(request.data))
            return Response({"details": "Either seller code or product name or product id or id is missing.",
                             "status_code": "MISSING_REQUIRED_FIELDS"},
                            status.HTTP_200_OK)
        update_user_product(seller_code, product_name, product_serial_no, user_id, id)
        return Response({"details": "Product updated successfully.",
                         "status_code": "SUCCESS"},
                        status.HTTP_200_OK)


class MyProductsViewSet(BaseModelViewSet):
    serializer_class = get_user_products_serializer()

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return get_user_products(user_id)

