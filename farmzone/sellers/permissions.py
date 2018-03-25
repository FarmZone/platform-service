import logging

from rest_framework import permissions
from farmzone.sellers.models import SellerOwner, Seller

logger = logging.getLogger(__name__)


class SellerPermission(permissions.BasePermission):
    message = 'Un-authorized access'

    def has_permission(self, request, view):
        user = request.user
        seller_code = request.parser_context['kwargs'].get('seller_code')
        authenticated = user.is_authenticated() and user.is_active
        if not authenticated: return False
        # Must be some old API, can only access data for the current user
        if not seller_code: return False

        if SellerOwner.objects.filter(user_id=user.id, seller__seller_code=seller_code).exists():
            return True
        # elif any([user.is_state_head(), user.is_franchisee_owner()]) \
        #     and Seller.objects.filter(seller_code=seller_code).exists():
        #     # May be user is trying to make call on behalf of some other supplier
        #     return True
        return False
