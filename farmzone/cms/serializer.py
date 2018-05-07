from rest_framework import serializers
from farmzone.sellers.models import UserProduct
from farmzone.sellers.serializers import SellerSerializer


class UserProductsSerializer(serializers.ModelSerializer):
    seller = SellerSerializer()
    product_name = serializers.CharField
    product_serial_no = serializers.CharField

    class Meta:
        model = UserProduct
        fields = ('seller', 'product_name', 'product_serial_no')
