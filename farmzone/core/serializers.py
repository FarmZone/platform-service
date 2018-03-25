from rest_framework import serializers
from farmzone.core.models import User, PhoneNumber
from farmzone.sellers.models import SellerOwner


class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumber
        fields = ("phone_number", "type", "is_primary", "user")


class UserSerializer(serializers.ModelSerializer):
    phone_number = serializers.SerializerMethodField()
    img_orig = serializers.SerializerMethodField()
    img_thumb = serializers.SerializerMethodField()
    seller_code = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("full_name", "id", "email", "phone_number", "is_admin", "img_orig", "img_thumb", "seller_code")

    def get_phone_number(self, obj):
        return obj.get_phone_number()

    def get_img_orig(self, obj):
        return str(obj.get_img_orig())

    def get_img_thumb(self, obj):
        return str(obj.get_img_orig())

    def get_seller_code(self, obj):
        seller_owner = SellerOwner.objects.select_related('seller').filter(user=obj).first()
        if seller_owner:
            return str(seller_owner.seller.seller_code)
        else:
            return ''
