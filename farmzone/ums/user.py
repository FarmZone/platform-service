from farmzone.sellers.models import PreferredSeller
import logging
logger = logging.getLogger(__name__)


def get_seller_preferred_users(seller_code):
    return PreferredSeller.objects.filter(seller__seller_code=seller_code)