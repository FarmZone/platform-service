from __future__ import unicode_literals, absolute_import

from django.conf.urls import url
from farmzone.core.views.views import LegalPolicyView


urlpatterns = [
    url(r'core/legal_policy/?$', LegalPolicyView.as_view()),
]
