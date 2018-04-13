from __future__ import unicode_literals, absolute_import

from django.conf.urls import url
from farmzone.buyers.views.order import CartDetailView, BuyerUpcomingOrdersView, BuyerCompletedOrdersView
from farmzone.buyers.views.product import BuyerProductsByCategoryView, BuyerProductsSummaryView, BuyerProductDetailView
from farmzone.buyers.views.support import BuyerPendingQueriesViewSet, BuyerResolvedQueriesViewSet

urlpatterns = [
    url(r'buyer/(?P<user_id>[\w]+)/cart_detail/?$', CartDetailView.as_view()),
    url(r'buyer/(?P<user_id>[\w]+)/upcoming_orders/?$', BuyerUpcomingOrdersView.as_view()),
    url(r'buyer/(?P<user_id>[\w]+)/completed_orders/?$', BuyerCompletedOrdersView.as_view()),
    url(r'buyer/(?P<user_id>[\w]+)/products_summary/?$', BuyerProductsSummaryView.as_view()),
    url(r'buyer/(?P<user_id>[\w]+)/products_by_category/(?P<category_code>[\w]+)/?$', BuyerProductsByCategoryView.as_view()),
    url(r'buyer/(?P<user_id>[\w]+)/product_detail/(?P<product_code>[\w]+)/?$', BuyerProductDetailView.as_view()),
    url(r'buyer/(?P<user_id>[\w]+)/pending_queries/?$', BuyerPendingQueriesViewSet.as_view({'get': 'list'})),
    url(r'buyer/(?P<user_id>[\w]+)/resolved_queries/?$', BuyerResolvedQueriesViewSet.as_view({'get': 'list'})),
]
