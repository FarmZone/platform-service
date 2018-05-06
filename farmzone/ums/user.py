from farmzone.sellers.models import PreferredSeller
from farmzone.ums.serializers import PreferredSellerSerializer, UserSellersSerializer
import logging
logger = logging.getLogger(__name__)


def get_seller_preferred_users(seller_code):
    return PreferredSeller.objects.filter(seller__seller_code=seller_code)


def get_seller_preferred_users_serializer():
    return PreferredSellerSerializer


def get_seller_by_user(user_id):
    return PreferredSeller.objects.filter(user_id=user_id).select_related("seller").first().seller


def get_user_sellers(user_id):
    return PreferredSeller.objects.filter(user_id=user_id)


def get_user_sellers_serializer():
    return UserSellersSerializer