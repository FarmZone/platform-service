from celery.utils.log import get_task_logger
from push_notifications.models import GCMDevice
log = get_task_logger(__name__)


NOTIFICATION_STATUS_CODE = {
    'notification_sent': 'NOTIFICATION_SENT',
    'notification_failed': 'SENDING_NOTIFICATION_FAILED'
}


class NotificationResponse:

    def __init__(self, status, details, message=None):
        self.status = status
        self.details = details
        self.message = message

    def __str__(self):
        return "Status: {0}, Details: {1}".format(self.status, self.details)

    @staticmethod
    def build_response(status, details, message=None):
        return NotificationResponse(status, details, message)


class NotificationClient:

    def send_notification_with_title(self, registration_id_list, body=None, title=None, message=None):
        registration_ids = registration_id_list
        if not isinstance(registration_id_list, list):
            registration_ids = [registration_id_list]
        send_to_device = GCMDevice.objects.filter(registration_id__in=registration_ids)
        if send_to_device:
            sent_message = send_to_device.send_message(message, title=title, extra=body)
            log.info("Notification client send message response {0}".format(sent_message))
            sent_message = sent_message[0] if isinstance(sent_message, list) and sent_message else sent_message
            if not sent_message.get("success"):
                return NotificationResponse(NOTIFICATION_STATUS_CODE.get('notification_failed'), sent_message.get("results"))
            else:
                return NotificationResponse(NOTIFICATION_STATUS_CODE.get('notification_sent'), sent_message.get("results"))


notification_client = NotificationClient()
