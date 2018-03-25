from __future__ import unicode_literals, absolute_import

from django.conf.urls import url
from farmzone.sellers.views.product import SellerProductsSummaryView, SellerProductsByCategoryView\
    , SellerProductDetailView
from farmzone.sellers.views.user import SellerPreferredUserViewSet


urlpatterns = [
    url(r'seller/(?P<seller_code>[\w]+)/products_summary/?$', SellerProductsSummaryView.as_view()),
    url(r'seller/(?P<seller_code>[\w]+)/products_by_category/(?P<category_code>[\w]+)/?$', SellerProductsByCategoryView.as_view()),
    url(r'seller/(?P<seller_code>[\w]+)/product_detail/(?P<product_code>[\w]+)/?$', SellerProductDetailView.as_view()),
    url(r'seller/(?P<seller_code>[\w]+)/preferred_users/?$', SellerPreferredUserViewSet.as_view({'get': 'list'})),
]
