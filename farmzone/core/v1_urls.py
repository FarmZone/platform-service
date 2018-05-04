from __future__ import unicode_literals, absolute_import

from django.conf.urls import url
from farmzone.core.views.views import LegalPolicyView, AboutUsView


urlpatterns = [
    url(r'core/legal_policy/?$', LegalPolicyView.as_view()),
    url(r'core/about_us/?$', AboutUsView.as_view()),
]
