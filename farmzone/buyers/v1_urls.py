from __future__ import unicode_literals, absolute_import

from django.conf.urls import url
from farmzone.buyers.views.order import BuyerUpcomingOrdersView, BuyerCompletedOrdersView, PlaceOrder, CancelOrder\
    , SaveOrderRatingView, CompleteOrderView
from farmzone.buyers.views.product import BuyerProductsByCategoryView, BuyerProductsSummaryView, BuyerProductDetailView\
    , AddMyProduct, MyProductsViewSet, UpdateMyProduct
from farmzone.buyers.views.support import BuyerPendingQueriesViewSet, BuyerResolvedQueriesViewSet, SaveQueryView, ResolveQueryView
from farmzone.buyers.views.cart import CartDetailView, AddToCartView
from farmzone.buyers.views.user import MySellersViewSet, UnassociatedSellersView, AddSellerView

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
    url(r'buyer/(?P<user_id>[\w]+)/resolve_query/?$', ResolveQueryView.as_view()),
    url(r'buyer/(?P<user_id>[\w]+)/save_order_rating/?$', SaveOrderRatingView.as_view()),
    url(r'buyer/(?P<user_id>[\w]+)/complete_order/?$', CompleteOrderView.as_view()),
    url(r'buyer/(?P<user_id>[\w]+)/my_sellers/?$', MySellersViewSet.as_view({'get': 'list'})),
    url(r'buyer/(?P<user_id>[\w]+)/add_my_product/?$', AddMyProduct.as_view()),
    url(r'buyer/(?P<user_id>[\w]+)/my_products/?$', MyProductsViewSet.as_view({'get': 'list'})),
    url(r'buyer/(?P<user_id>[\w]+)/update_my_product/?$', UpdateMyProduct.as_view()),
    url(r'buyer/(?P<user_id>[\w]+)/get_unassociated_sellers/?$', UnassociatedSellersView.as_view()),
    url(r'buyer/(?P<user_id>[\w]+)/add_seller/?$', AddSellerView.as_view()),
]
