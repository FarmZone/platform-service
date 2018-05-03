from __future__ import unicode_literals, absolute_import

from django.conf.urls import url
from farmzone.buyers.views.order import BuyerUpcomingOrdersView, BuyerCompletedOrdersView, PlaceOrder, CancelOrder
from farmzone.buyers.views.product import BuyerProductsByCategoryView, BuyerProductsSummaryView, BuyerProductDetailView
from farmzone.buyers.views.support import BuyerPendingQueriesViewSet, BuyerResolvedQueriesViewSet, SaveQueryView
from farmzone.buyers.views.cart import CartDetailView, AddToCartView

urlpatterns = [
    url(r'buyer/(?P<user_id>[\w]+)/cart_detail/?$', CartDetailView.as_view()),
    url(r'buyer/(?P<user_id>[\w]+)/add_to_cart/?$', AddToCartView.as_view()),
    url(r'buyer/(?P<user_id>[\w]+)/place_order/?$', PlaceOrder.as_view()),
    url(r'buyer/(?P<user_id>[\w]+)/cancel_order/?$', CancelOrder.as_view()),
    url(r'buyer/(?P<user_id>[\w]+)/upcoming_orders/?$', BuyerUpcomingOrdersView.as_view()),
    url(r'buyer/(?P<user_id>[\w]+)/completed_orders/?$', BuyerCompletedOrdersView.as_view()),
    url(r'buyer/(?P<user_id>[\w]+)/products_summary/?$', BuyerProductsSummaryView.as_view()),
    url(r'buyer/(?P<user_id>[\w]+)/products_by_category/(?P<category_code>[\w]+)/?$', BuyerProductsByCategoryView.as_view()),
    url(r'buyer/(?P<user_id>[\w]+)/product_detail/(?P<product_code>[\w]+)/?$', BuyerProductDetailView.as_view()),
    url(r'buyer/(?P<user_id>[\w]+)/pending_queries/?$', BuyerPendingQueriesViewSet.as_view({'get': 'list'})),
    url(r'buyer/(?P<user_id>[\w]+)/resolved_queries/?$', BuyerResolvedQueriesViewSet.as_view({'get': 'list'})),
    url(r'buyer/(?P<user_id>[\w]+)/save_query/?$', SaveQueryView.as_view()),
]
