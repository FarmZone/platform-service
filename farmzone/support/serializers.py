from rest_framework import serializers
from farmzone.support.models import Support, SupportCategory
from farmzone.core.serializers import UserSerializer


class SupportCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = SupportCategory
        fields = ("id", "name", "description")


class SupportSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    comment = serializers.SerializerMethodField()
    status = serializers.CharField
    id = serializers.IntegerField
    support_category = SupportCategorySerializer()

    class Meta:
        model = Support
        fields = ('user', 'comment', 'status', 'support_category', 'id')

    def get_comment(self, obj):
        support_category = obj.support_category
        return support_category.name if support_category.id!=999 else obj.comment
