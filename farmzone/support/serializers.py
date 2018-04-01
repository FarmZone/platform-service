from rest_framework import serializers
from farmzone.support.models import Support
from farmzone.core.serializers import UserSerializer


class SupportSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Support
        fields = ('user',)

