from django.test import TestCase
from django.test import override_settings
from farmzone.sellers.models import Seller


@override_settings(CELERY_ALWAYS_EAGER=True)
class TestSellerAPI(TestCase):
    def setUp(self):
        Seller.objects.create(name="TestSeller", is_active=True)

    def test_seller_object(self):
        seller = Seller.objects.get(name="TestSeller")
        self.assertEqual(seller.is_active, True)
