from django.db import models
from farmzone.core.models import TimestampedModel, User
from push_notifications.models import GCMDevice


class BuyerDevice(TimestampedModel):
    user = models.ForeignKey(User)
    fcm_device = models.ForeignKey(GCMDevice)

    class Meta:
        db_table = "buyer_device"
        verbose_name = "Buyer Device"
        verbose_name_plural = "Buyer Devices"

    def __str__(self):
        return "{0}#{1}".format(self.user.full_name, self.fcm_device)

    @classmethod
    def add_or_update_buyer_device(cls, user, registration_id):
        buyer_device = BuyerDevice.objects.filter(user=user).first()
        if buyer_device:
            buyer_device.fcm_device.registration_id = registration_id
            buyer_device.fcm_device.active = 1
            buyer_device.fcm_device.save()
        else:
            new_device = GCMDevice.objects.create(
                name=user.username,
                active=1,
                registration_id=registration_id,
                cloud_message_type='FCM'
            )
            BuyerDevice.objects.create(
                user=user,
                fcm_device=new_device
            )
