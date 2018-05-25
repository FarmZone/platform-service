from farmzone.core.models import User
from farmzone.sellers.models import SellerDevice
from farmzone.buyers.models import BuyerDevice
from farmzone.util_config.celery import app
from celery.utils.log import get_task_logger
from farmzone.util_config.translation_util import get_locale_based_template
from farmzone.notification.sms import sms_provider
from farmzone.notification.notification_client import notification_client
from farmzone.notification.constants import get_seller_order_notification_type, get_buyer_order_notification_type\
    , get_buyer_complain_notification_type, get_seller_complain_notification_type
from farmzone.support.serializers import SupportSerializer
from farmzone.support.models import Support
import json

logger = get_task_logger(__name__)

TITLE = "A3Agri"
BUYER_DEVICE = "BUYER_DEVICE"
SELLER_DEVICE = "SELLER_DEVICE"


def send_sms_to_user(user, key, **kwargs):
    send_sms_to_user_id(user.id, key, **kwargs)


def send_sms_to_user_id(user_id, key, **kwargs):
    logger.info("Scheduling task to send SMS to user_id {0}".format(user_id))
    try:
        notify_user.delay(user_id, key, **kwargs)
    except Exception as e:
        logger.error("Not able to schedule send sms {0}".format(e))


@app.task
def notify_user(uid, sms_template_key, *args, **kwargs):
    user = User.objects.filter(id=uid).first()
    if not user:
        logger.error("Invalid user_id: {0}. Not sending sms.".format(uid))
        return
    if not user.is_active:
        logger.error("Inactive user_id: {0}. Not sending sms.".format(uid))
        return
    phone_number = user.get_phone_number()
    if not phone_number:
        logger.error("No phone number found for the user_id: {0}. Not sending sms.".format(uid))
        return

    preferred_locale = 'en'
    logger.debug("Sending SMS to user: {0}, in his preferred_local: {1}".format(user.full_name, preferred_locale))
    sms_body = get_locale_based_template(sms_template_key, preferred_locale)
    sms_body = sms_body.format(*args, **kwargs)
    logger.debug("Sending Transactional SMS {0} to number {1}".format(sms_body, phone_number))
    sms_provider.send_transactional_sms(phone_number, sms_body)
    logger.debug("SMS has been sent on number: {0}".format(phone_number))


@app.task
def notify_app_user(uid, device, title, message, body):
    user = User.objects.filter(id=uid).first()
    if not user:
        logger.error("Invalid user_id: {0}. Not sending notification.".format(uid))
        return
    if not user.is_active:
        logger.error("Inactive user_id: {0}. Not sending notification.".format(uid))
        return
    user_device = None
    if device == BUYER_DEVICE:
        user_device = BuyerDevice.objects.filter(user_id=uid).first()
    elif device == SELLER_DEVICE:
        user_device = SellerDevice.objects.filter(user_id=uid).first()
    if not user_device:
        logger.error("No device found for the user_id: {0}. Not sending notification.".format(uid))
        return
    logger.debug('Notification content for user {0} is {1}'.format(uid, body))
    logger.debug("Message content for user {0} is {1} with title {2}".format(uid, message, title))
    notification_response = notification_client.send_notification_with_title(
        user_device.fcm_device.registration_id,
        body=body,
        title=title,
        message=message
    )
    logger.debug('Notification response for user {0} is {1}'.format(uid, notification_response))


def send_buyer_order_notification(user_id, order_id, order_status):
    message = get_buyer_order_notification_type(order_id, order_status)
    body = get_serialized_order_by_id(order_id)
    send_app_notification_to_user_id(user_id, BUYER_DEVICE, TITLE, message, body)


def send_seller_order_notification(user_id, order_id, order_status):
    message = get_seller_order_notification_type(order_id, order_status)
    body = get_serialized_order_by_id(order_id)
    send_app_notification_to_user_id(user_id, SELLER_DEVICE, TITLE, message, body)


def send_buyer_complain_notification(user_id, query_id, query_status):
    message = get_buyer_complain_notification_type(query_id, query_status)
    body = get_serialized_query_by_id(query_id)
    send_app_notification_to_user_id(user_id, BUYER_DEVICE, TITLE, message, body)


def send_seller_complain_notification(user_id, query_id, query_status):
    message = get_seller_complain_notification_type(query_id, query_status)
    body = get_serialized_query_by_id(query_id)
    send_app_notification_to_user_id(user_id, SELLER_DEVICE, TITLE, message, body)


def send_app_notification_to_user_id(user_id, device, title, message, body):
    logger.info("Scheduling task to send app notification to user_id {0}".format(user_id))
    try:
        logger.debug('Notification content for user {0} is {1}'.format(user_id, body))
        logger.debug("Message content for user {0} is {1} with title {2}".format(user_id, message, title))
        notify_app_user.delay(user_id, device, title, message, body)
    except Exception as e:
        logger.error("Not able to schedule send notification {0}".format(e))


def get_serialized_query_by_id(query_id):
    if not query_id:
        return
    support = Support.objects.filter(id=query_id).first()
    if not support:
        return
    stringified = json.dumps(SupportSerializer(support).data)
    body = {"query_details": json.loads(stringified)}
    return body


def get_serialized_order_by_id(order_id):
    if not order_id:
        return
    # stringified = json.dumps(SupportSerializer(support).data)
    # body = {"query_details": json.loads(stringified)}
    body = {"order_details": {"id":order_id}}
    return body