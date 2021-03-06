from __future__ import unicode_literals, absolute_import

from django.conf.urls import url
from farmzone.sellers.views.product import SellerProductsSummaryView, SellerProductsByCategoryView\
    , SellerProductDetailView
from farmzone.sellers.views.user import SellerPreferredUserViewSet, RegisterSellerDeviceView
from farmzone.sellers.views.order import SellerUpcomingOrdersView, SellerCompletedOrdersView, AcceptOrderView, DispatchOrderView
from farmzone.sellers.views.support import SellerPendingQueriesViewSet, SellerResolvedQueriesViewSet, AcceptQueryView


urlpatterns = [
    url(r'seller/(?P<seller_code>[\w]+)/products_summary/?$', SellerProductsSummaryView.as_view()),
    url(r'seller/(?P<seller_code>[\w]+)/products_by_category/(?P<category_code>[\w]+)/?$', SellerProductsByCategoryView.as_view()),
    url(r'seller/(?P<seller_code>[\w]+)/product_detail/(?P<product_code>[\w]+)/?$', SellerProductDetailView.as_view()),
    url(r'seller/(?P<seller_code>[\w]+)/preferred_users/?$', SellerPreferredUserViewSet.as_view({'get': 'list'})),
    url(r'seller/(?P<seller_code>[\w]+)/upcoming_orders/?$', SellerUpcomingOrdersView.as_view()),
    url(r'seller/(?P<seller_code>[\w]+)/completed_orders/?$', SellerCompletedOrdersView.as_view()),
    url(r'seller/(?P<seller_code>[\w]+)/pending_queries/?$', SellerPendingQueriesViewSet.as_view({'get': 'list'})),
    url(r'seller/(?P<seller_code>[\w]+)/resolved_queries/?$', SellerResolvedQueriesViewSet.as_view({'get': 'list'})),
    url(r'seller/(?P<seller_code>[\w]+)/accept_query/?$', AcceptQueryView.as_view()),
    url(r'seller/(?P<seller_code>[\w]+)/accept_order/?$', AcceptOrderView.as_view()),
    url(r'seller/(?P<seller_code>[\w]+)/dispatch_order/?$', DispatchOrderView.as_view()),
    url(r'seller/(?P<seller_code>[\w]+)/register_seller_device/?$', RegisterSellerDeviceView.as_view()),
]
