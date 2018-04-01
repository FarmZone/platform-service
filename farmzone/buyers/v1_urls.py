from __future__ import unicode_literals, absolute_import

from django.conf.urls import url
from farmzone.buyers.views.order import CartDetailView, OrderDetailView, OrderView


urlpatterns = [
    url(r'buyer/(?P<user_id>[\w]+)/cart_detail/?$', CartDetailView.as_view()),
    url(r'buyer/(?P<user_id>[\w]+)/orders/?$', OrderView.as_view()),
    url(r'buyer/(?P<user_id>[\w]+)/order_detail/?$', OrderDetailView.as_view()),
]
