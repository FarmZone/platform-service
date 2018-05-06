from rest_framework import serializers
from farmzone.sellers.models import PreferredSeller
from farmzone.core.serializers import UserSerializer
from farmzone.sellers.serializers import SellerSerializer


class PreferredSellerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = PreferredSeller
        fields = ('user',)


class UserSellersSerializer(serializers.ModelSerializer):
    seller = SellerSerializer()

    class Meta:
        model = PreferredSeller
        fields = ('seller',)

