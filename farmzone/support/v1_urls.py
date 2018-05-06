from __future__ import unicode_literals, absolute_import

from django.conf.urls import url
from farmzone.support.views.views import SupportCategoryViewSet, OrderSupportCategoryViewSet


urlpatterns = [
    url(r'support/get_query_support_categories/?$', SupportCategoryViewSet.as_view({'get': 'list'})),
    url(r'support/get_order_support_categories/?$', OrderSupportCategoryViewSet.as_view({'get': 'list'})),
]
