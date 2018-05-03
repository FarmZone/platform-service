from rest_framework import serializers
from farmzone.support.models import Support, SupportCategory
from farmzone.core.serializers import UserSerializer


class SupportCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = SupportCategory
        fields = ("id", "name", "description")


class SupportSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    comment = serializers.CharField
    status = serializers.CharField
    support_category = SupportCategorySerializer()

    class Meta:
        model = Support
        fields = ('user', 'comment', 'status', 'support_category')
