from rest_framework import serializers
from farmzone.sellers.models import Seller, UserProduct


class SellerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Seller
        fields = ("seller_code", "name")
