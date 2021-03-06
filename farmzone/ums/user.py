from farmzone.sellers.models import PreferredSeller, Seller, SellerDevice
from farmzone.buyers.models import BuyerDevice
from farmzone.ums.serializers import PreferredSellerSerializer, UserSellersSerializer
from farmzone.util_config.custom_exceptions import CustomAPI400Exception
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


def get_user_unassociated_sellers(user_id, q):
    return Seller.objects.filter(is_active=True, name__icontains=q).exclude(preferredseller__user__id=user_id).values("seller_code", "name")


def add_seller(seller_code, user_id):
    seller = Seller.objects.filter(seller_code=seller_code).first()
    if not seller:
        logger.info("Seller not found for given code {0}".format(seller_code))
        raise CustomAPI400Exception({
            "details": "Seller code is not valid.",
            "status_code": "INVALID_REQUIRED_FIELDS"
        })
    duplicate = PreferredSeller.objects.filter(seller=seller, user_id=user_id).first()
    if duplicate:
        logger.info("Seller code already exists {0}".format(seller_code))
        raise CustomAPI400Exception({
            "details": "This seller is already associated.",
            "status_code": "INVALID_REQUIRED_FIELDS"
        })
    PreferredSeller.add_seller(seller, user_id)


def register_seller_device(user, seller_code, registration_id):
    seller = Seller.objects.filter(seller_code=seller_code).first()
    if not seller:
        logger.info("Seller not found for given code {0}".format(seller_code))
        raise CustomAPI400Exception({
            "details": "Seller code is not valid.",
            "status_code": "INVALID_REQUIRED_FIELDS"
        })
    SellerDevice.add_or_update_seller_device(user, registration_id)


def register_buyer_device(user, user_id, registration_id):
    BuyerDevice.add_or_update_buyer_device(user, registration_id)
