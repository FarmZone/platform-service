import logging
from django.views import View
from django.shortcuts import render

logger = logging.getLogger(__name__)


class LegalPolicyView(View):

    def get(self, request, app_version=None):
        return render(request, "core/legal_policy.html", context={})
