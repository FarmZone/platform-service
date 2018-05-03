from __future__ import unicode_literals, absolute_import

from django.conf.urls import url
from farmzone.support.views.views import SupportCategoryViewSet


urlpatterns = [
    url(r'support/get_support_categories/?$', SupportCategoryViewSet.as_view({'get': 'list'})),
]
