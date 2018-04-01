import logging
from rest_framework import permissions
logger = logging.getLogger(__name__)


class BuyerPermission(permissions.BasePermission):
    message = 'Un-authorized access'

    def has_permission(self, request, view):
        user_id = request.parser_context['kwargs'].get('user_id')
        if user_id:
            user_id = int(user_id)
        user = request.user
        logger.debug("user_id in url {0} and logedin user {1}".format(user_id, user.id))
        authenticated = user.is_authenticated() and user.is_active and user.id == user_id
        if not authenticated: return False
        return True
