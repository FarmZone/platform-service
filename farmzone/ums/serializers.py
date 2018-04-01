from rest_framework import serializers
from farmzone.sellers.models import PreferredSeller
from farmzone.core.serializers import UserSerializer


class PreferredSellerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = PreferredSeller
        fields = ('user',)

