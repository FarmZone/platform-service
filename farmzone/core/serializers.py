from rest_framework import serializers
from farmzone.core.models import User, PhoneNumber, Address
from farmzone.sellers.models import SellerOwner


class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumber
        fields = ("phone_number", "type", "is_primary", "user")


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = ("address_line1", "address_line2", "address_lin3", "status")


class UserSerializer(serializers.ModelSerializer):
    phone_number = serializers.SerializerMethodField()
    img_orig = serializers.SerializerMethodField()
    img_thumb = serializers.SerializerMethodField()
    seller = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("full_name", "id", "email", "phone_number", "is_admin", "img_orig", "img_thumb"
                  , "seller", "address")
        depth = 2

    def get_phone_number(self, obj):
        return obj.get_phone_number()

    def get_img_orig(self, obj):
        return str(obj.get_img_orig())

    def get_img_thumb(self, obj):
        return str(obj.get_img_orig())

    def get_seller(self, obj):
        seller_owner = SellerOwner.objects.select_related('seller').filter(user=obj).first()
        if seller_owner:
            return {"seller_code":seller_owner.seller.seller_code, "seller_name":seller_owner.seller.name}
        else:
            return {}

    def get_address(self, obj):
        address = Address.objects.select_related("state").filter(user=obj).first()
        if address:
            return {"address_line1":address.address_line1, "address_line2":address.address_line2
                , "address_line3":address.address_line3, "state":address.state.name}
        else:
            return {}

